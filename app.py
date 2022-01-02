import os
import re
import sys
import random

from flask import Flask, request, abort, send_file, redirect
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
  MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)

from fsm.fsm import TaipeiMRTMachine, find_station

load_dotenv()

machines = {}
MACHINE = TaipeiMRTMachine()

app = Flask(__name__, static_url_path='')

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
  print('Specify LINE_CHANNEL_SECRET as environment variable.')
  sys.exit(1)
if channel_access_token is None:
  print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
  sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

ROUTE_NAME_DICT = {
  'ho': '家',
  'BR': '文湖線',
  'R': '淡水信義線',
  'R2': '新北投支線',
  'G': '松山新店線',
  'G0': '小碧潭支線',
  'O': '中和新蘆線',
  'BL': '板南線',
  'Y': '環狀線',
}

COLOR_DICT = {
  'ho': '#8daad9',
  'BR': '#c48c31',
  'R': '#e3002c',
  'R2': '#fd92a3',
  'G': '#008659',
  'G0': '#cfdb00',
  'O': '#f8b61c',
  'BL': '#0070bd',
  'Y': '#ffdb00',
}

FG_COLOR_DICT = {
  'ho': '#000000',
  'BR': '#ffffff',
  'R': '#ffffff',
  'R2': '#000000',
  'G': '#ffffff',
  'G0': '#000000',
  'O': '#000000',
  'BL': '#ffffff',
  'Y': '#000000',
}

OPTION_TO_ZH_DICT = {'get_off': '下車', 'continue': '繼續搭乘'}

ZH_TO_OPTION_DICT = {'下車': 'get_off', '繼續搭乘': 'continue'}

HOME_IMAGE_URL = 'https://news-secr.ncku.edu.tw/var/file/37/1037/pictures/251/m/mczh-tw1000x1000_large41985_177280320869.jpg'


def current_state_to_send_message(machine: TaipeiMRTMachine):
  current_state = machine.state
  if current_state == 'home':
    return FlexSendMessage(
      alt_text=machine.info_str,
      contents={
        'type': 'bubble',
        'hero':
          {
            'type': 'image',
            'url': HOME_IMAGE_URL,
            'size': 'full',
            'aspectRatio': '20:13',
            'aspectMode': 'cover',
          },
        'body':
          {
            'type':
              'box',
            'layout':
              'vertical',
            'contents':
              [
                {
                  'type': 'text',
                  'text': '家',
                  'align': 'center',
                  'weight': 'bold',
                  'size': 'xl'
                }, {
                  'type': 'text',
                  'text': machine.info_str,
                  'align': 'center',
                  'size': 'md'
                }
              ]
          },
        'footer':
          {
            'type': 'box',
            'layout': 'vertical',
            'spacing': 'sm',
            'contents':
              [
                {
                  'type': 'button',
                  'style': 'link',
                  'height': 'sm',
                  'action':
                    {
                      'type': 'message',
                      'label': '隨機旅行',
                      'text': '隨機旅行',
                    }
                }
              ],
            'flex': 0
          }
      }
    )
  elif '->' in current_state:
    options = sorted(machine.options)
    options.reverse()
    terminal_station = current_state.split('->')[1].split('(')[0]
    current_station = current_state.split('->')[0]
    transitions = machine.get_transitions('continue', machine.state)
    if len(transitions) > 0:
      next_station = transitions[0].dest.split('->')[0]
    else:
      next_station = None
    terminal_station_code = current_state.split('->')[1].split('('
                                                              )[1].split(')')[0]
    color = COLOR_DICT[terminal_station_code[:-2]]
    word_color = FG_COLOR_DICT[terminal_station_code[:-2]]
    route_name = ROUTE_NAME_DICT[terminal_station_code[:-2]]
    body_box_contents = [
      {
        'type': 'text',
        'text': '終點站：' + terminal_station,
        'align': 'center',
        'weight': 'bold',
        'size': 'sm',
        'wrap': True,
        'color': '#666666'
      }, {
        'type': 'box',
        'layout': 'vertical',
        'contents': [],
        'height': '16px'
      }, {
        'type': 'box',
        'layout': 'horizontal',
        'contents':
          [
            {
              'type': 'box',
              'layout': 'baseline',
              'contents': [{
                'type': 'filler'
              }],
              'flex': 1
            }, {
              'type': 'box',
              'layout': 'vertical',
              'contents':
                [
                  {
                    'type': 'box',
                    'layout': 'horizontal',
                    'contents':
                      [
                        {
                          'type': 'filler'
                        }, {
                          'type': 'box',
                          'layout': 'vertical',
                          'contents': [],
                          'width': '2px',
                          'backgroundColor': '#c0c0c0'
                        }, {
                          'type': 'filler'
                        }
                      ],
                    'flex': 1,
                    'width': '14px'
                  }
                ],
              'width': '14px'
            }, {
              'type': 'box',
              'layout': 'vertical',
              'contents': [],
              'flex': 4
            }
          ],
        'spacing': 'lg',
        'height': '40px'
      }, {
        'type': 'box',
        'layout': 'horizontal',
        'contents':
          [
            {
              'type': 'box',
              'layout': 'horizontal',
              'contents':
                [
                  {
                    'type':
                      'text',
                    'text':
                      '本站' if current_station != terminal_station else '終點站',
                    'gravity':
                      'center',
                    'size':
                      'sm',
                    'weight':
                      'bold'
                  }
                ],
              'flex': 1
            }, {
              'type': 'box',
              'layout': 'vertical',
              'contents':
                [
                  {
                    'type': 'filler'
                  }, {
                    'type': 'box',
                    'layout': 'vertical',
                    'contents': [],
                    'cornerRadius': '30px',
                    'width': '12px',
                    'height': '12px',
                    'backgroundColor': color
                  }, {
                    'type': 'filler'
                  }
                ],
              'width': '14px',
              'flex': 0
            }, {
              'type': 'text',
              'text': current_station,
              'gravity': 'center',
              'flex': 4,
              'size': 'sm',
              'weight': 'bold'
            }
          ],
        'spacing': 'lg',
        'cornerRadius': '30px'
      }
    ]
    if machine.info_str:
      body_box_contents.insert(
        1, {
          'type': 'text',
          'text': machine.info_str,
          'align': 'center',
          'weight': 'bold',
          'size': 'sm',
          'wrap': True,
          'color': '#666666'
        }
      )
    if next_station:
      body_box_contents.append(
        {
          'type': 'box',
          'layout': 'horizontal',
          'contents':
            [
              {
                'type': 'box',
                'layout': 'baseline',
                'contents': [{
                  'type': 'filler'
                }],
                'flex': 1
              }, {
                'type': 'box',
                'layout': 'vertical',
                'contents':
                  [
                    {
                      'type': 'box',
                      'layout': 'horizontal',
                      'contents':
                        [
                          {
                            'type': 'filler'
                          }, {
                            'type': 'box',
                            'layout': 'vertical',
                            'contents': [],
                            'width': '2px',
                            'backgroundColor': color
                          }, {
                            'type': 'filler'
                          }
                        ],
                      'flex': 1,
                      'width': '14px'
                    }
                  ],
                'width': '14px'
              }, {
                'type': 'box',
                'layout': 'vertical',
                'contents': [],
                'flex': 4
              }
            ],
          'spacing': 'lg',
          'height': '64px'
        }
      )
      body_box_contents.append(
        {
          'type': 'box',
          'layout': 'horizontal',
          'contents':
            [
              {
                'type': 'text',
                'text': '下一站',
                'gravity': 'center',
                'size': 'sm'
              }, {
                'type': 'box',
                'layout': 'vertical',
                'contents':
                  [
                    {
                      'type': 'filler'
                    }, {
                      'type': 'box',
                      'layout': 'vertical',
                      'contents': [],
                      'cornerRadius': '30px',
                      'width': '12px',
                      'height': '12px',
                      'borderColor': color,
                      'borderWidth': '2px'
                    }, {
                      'type': 'filler'
                    }
                  ],
                'width': '14px',
                'flex': 0
              }, {
                'type': 'text',
                'text': next_station,
                'gravity': 'center',
                'flex': 4,
                'size': 'sm'
              }
            ],
          'spacing': 'lg',
          'cornerRadius': '30px'
        }
      )
    footer_contents = list(
      map(
        lambda x: {
          'type': 'button',
          'style': 'link',
          'height': 'sm',
          'action':
            {
              'type': 'message',
              'label': OPTION_TO_ZH_DICT[x],
              'text': OPTION_TO_ZH_DICT[x]
            }
        }, options
      )
    )
    return FlexSendMessage(
      alt_text=current_state,
      contents={
        'type': 'bubble',
        'size': 'mega',
        'header':
          {
            'type': 'box',
            'layout': 'vertical',
            'contents':
              [
                {
                  'type':
                    'box',
                  'layout':
                    'vertical',
                  'contents':
                    [
                      {
                        'type':
                          'text',
                        'text':
                          route_name + (
                            ''
                            if current_station != terminal_station else ' 終點站'
                          ),
                        'color':
                          word_color + 'c0',
                        'size':
                          'sm'
                      }, {
                        'type': 'text',
                        'text': current_station,
                        'color': word_color,
                        'size': 'xl',
                        'flex': 4,
                        'weight': 'bold'
                      }
                    ]
                }
              ],
            'paddingAll': '20px',
            'backgroundColor': color,
            'spacing': 'md',
            'paddingTop': '22px'
          },
        'body':
          {
            'type': 'box',
            'layout': 'vertical',
            'contents': body_box_contents
          },
        'footer':
          {
            'type': 'box',
            'layout': 'vertical',
            'contents': footer_contents
          }
      }
    )
  else:  # station
    options = machine.options
    options = options[:1] + sorted(options[1:])
    options.insert(1, None)
    footer_contents = list(
      map(
        lambda x: {
          'type':
            'button',
          'style':
            'link',
          'height':
            'sm',
          'action':
            {
              'type':
                'message',
              'label':
                (
                  '往' + find_station(x).name['zh'] + '(' + x + ')'
                  if x != 'home' else '回家'
                ) if '(' not in x else x + '(站外轉乘)',
              'text':
                (
                  '往' + find_station(x).name['zh'] + '(' + x + ')'
                  if x != 'home' else '回家'
                ) if '(' not in x else x.split('(')[1].split(')')[0]
            },
          'color':
            COLOR_DICT[x[:-2]]
            if '(' not in x else COLOR_DICT[x.split('(')[1][:-3]],
        } if x else {'type': 'separator'}, options
      )
    )
    footer_contents.append({'type': 'spacer', 'size': 'sm'})
    station_codes = machine.state.split('(')[1].split(')')[0].split(', ')
    header_box_box_contents = list(
      map(
        lambda x: {
          'type': 'box',
          'layout': 'vertical',
          'contents':
            [
              {
                'type': 'filler'
              }, {
                'type': 'text',
                'text': x,
                'color': FG_COLOR_DICT[x[:-2]],
                'size': 'xxl',
                'align': 'center',
                'gravity': 'center',
                'weight': 'bold'
              }, {
                'type': 'filler'
              }
            ],
          'cornerRadius': '42px',
          'height': '84px',
          'width': '84px',
          'backgroundColor': COLOR_DICT[x[:-2]]
        }, station_codes
      )
    )
    for i in range(0, len(station_codes) * 2 + 2, 2):
      header_box_box_contents.insert(i, {'type': 'filler'})
    return FlexSendMessage(
      alt_text=machine.info_str,
      contents={
        'type': 'bubble',
        'header':
          {
            'type': 'box',
            'layout': 'vertical',
            'contents':
              [
                {
                  'type': 'box',
                  'layout': 'horizontal',
                  'contents': header_box_box_contents
                }
              ],
            'spacing': 'md'
          },
        'body':
          {
            'type':
              'box',
            'layout':
              'vertical',
            'contents':
              [
                {
                  'type': 'text',
                  'text': current_state.split('(')[0],
                  'align': 'center',
                  'weight': 'bold',
                  'size': 'xxl'
                }, {
                  'type': 'text',
                  'text': machine.info_str,
                  'align': 'center',
                  'size': 'md'
                }
              ]
          },
        'footer':
          {
            'type': 'box',
            'layout': 'vertical',
            'spacing': 'sm',
            'contents': footer_contents,
            'flex': 0
          }
      }
    )


@app.route('/', methods=['GET'])
def root():
  return redirect('https://line.me/R/ti/p/%40578aojha', code=307)


@app.route('/callback', methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']
  # get request body as text
  body = request.get_data(as_text=True)
  app.logger.info('Request body: ' + body)

  # parse webhook body
  try:
    events = parser.parse(body, signature)
  except InvalidSignatureError:
    abort(400)

  # if event is MessageEvent and message is TextMessage, then echo text
  for event in events:
    if not isinstance(event, MessageEvent):
      continue
    if not isinstance(event.message, TextMessage):
      continue

    line_bot_api.reply_message(
      event.reply_token, TextSendMessage(text=event.message.text)
    )

  return 'OK'


@app.route('/webhook', methods=['POST'])
def webhook_handler():
  signature = request.headers['X-Line-Signature']
  # get request body as text
  body = request.get_data(as_text=True)
  app.logger.info(f'Request body: {body}')

  # parse webhook body
  try:
    events = parser.parse(body, signature)
  except InvalidSignatureError:
    abort(400)

  # if event is MessageEvent and message is TextMessage, then echo text
  for event in events:
    if not isinstance(event, MessageEvent):
      continue
    if not isinstance(event.message, TextMessage):
      continue
    if not isinstance(event.message.text, str):
      continue
    user_id = str(event.source.user_id)
    if user_id not in machines:
      machines.update({user_id: TaipeiMRTMachine()})
    machine = machines[user_id]
    options = machine.options
    print(f'\nFSM STATE: {machine.state}')
    print(f'REQUEST BODY: \n{body}')
    try:
      text = event.message.text
      if text == '回家':
        text = 'home'
      elif '往' == text[0] and machine.state != 'home':
        text = text.split('(')[1].split(')')[0]
      elif text in ZH_TO_OPTION_DICT and '->' in machine.state:
        text = ZH_TO_OPTION_DICT[text]

      if text == '隨機旅行' and machine.state == 'home':
        option = random.choice(options)
      else:
        option = next(
          option for option in options if text in re.split(' |,|\)|\(', option)
        )
      machine.trigger(str(option))
    except StopIteration:
      print('STATE NOT CHANGE')
    finally:
      line_bot_api.reply_message(
        event.reply_token, current_state_to_send_message(machine)
      )
      print(f'\nFSM STATE AFTER: {machine.state}')

  return 'OK'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
  filename = 'fsm.svg'
  if not os.path.isfile(filename):
    MACHINE.m.get_graph().draw(filename, prog='fdp')
  return send_file(filename, mimetype='image/svg+xml')


if __name__ == '__main__':
  port = os.environ.get('PORT', 8000)
  app.run(host='0.0.0.0', port=port, debug=True)
