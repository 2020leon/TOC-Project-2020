from transitions.extensions import GraphMachine


class Station:
  def __init__(self, codes: 'set[str]', name: 'dict[str, str]') -> None:
    self.codes = codes
    self.name = name
    self.routes = []
    self.out_of_station_transfers = []

  def __str__(self) -> str:
    return self.name['zh'] + '(' + ', '.join(sorted(self.codes)) + ')'


STATION_SET = {
  Station(codes={'BR01'}, name={'zh': '動物園'}),
  Station(codes={'BR02'}, name={'zh': '木柵'}),
  Station(codes={'BR03'}, name={'zh': '萬芳社區'}),
  Station(codes={'BR04'}, name={'zh': '萬芳醫院'}),
  Station(codes={'BR05'}, name={'zh': '辛亥'}),
  Station(codes={'BR06'}, name={'zh': '麟光'}),
  Station(codes={'BR07'}, name={'zh': '六張犁'}),
  Station(codes={'BR08'}, name={'zh': '科技大樓'}),
  Station(codes={'BR09', 'R05'}, name={'zh': '大安'}),
  Station(codes={'BR10', 'BL15'}, name={'zh': '忠孝復興'}),
  Station(codes={'BR11', 'G16'}, name={'zh': '南京復興'}),
  Station(codes={'BR12'}, name={'zh': '中山國中'}),
  Station(codes={'BR13'}, name={'zh': '松山機場'}),
  Station(codes={'BR14'}, name={'zh': '大直'}),
  Station(codes={'BR15'}, name={'zh': '劍南路'}),
  Station(codes={'BR16'}, name={'zh': '西湖'}),
  Station(codes={'BR17'}, name={'zh': '港墘'}),
  Station(codes={'BR18'}, name={'zh': '文德'}),
  Station(codes={'BR19'}, name={'zh': '內湖'}),
  Station(codes={'BR20'}, name={'zh': '大湖公園'}),
  Station(codes={'BR21'}, name={'zh': '葫洲'}),
  Station(codes={'BR22'}, name={'zh': '東湖'}),
  Station(codes={'BR23'}, name={'zh': '南港軟體園區'}),
  Station(codes={'BR24', 'BL23'}, name={'zh': '南港展覽館'}),
  Station(codes={'R02'}, name={'zh': '象山'}),
  Station(codes={'R03'}, name={'zh': '台北101／世貿'}),
  Station(codes={'R04'}, name={'zh': '信義安和'}),
  Station(codes={'R06'}, name={'zh': '大安森林公園'}),
  Station(codes={'R07', 'O06'}, name={'zh': '東門'}),
  Station(codes={'R08', 'G10'}, name={'zh': '中正紀念堂'}),
  Station(codes={'R09'}, name={'zh': '台大醫院'}),
  Station(codes={'R10', 'BL12'}, name={'zh': '台北車站'}),
  Station(codes={'R11', 'G14'}, name={'zh': '中山'}),
  Station(codes={'R12'}, name={'zh': '雙連'}),
  Station(codes={'R13', 'O11'}, name={'zh': '民權西路'}),
  Station(codes={'R14'}, name={'zh': '圓山'}),
  Station(codes={'R15'}, name={'zh': '劍潭'}),
  Station(codes={'R16'}, name={'zh': '士林'}),
  Station(codes={'R17'}, name={'zh': '芝山'}),
  Station(codes={'R18'}, name={'zh': '明德'}),
  Station(codes={'R19'}, name={'zh': '石牌'}),
  Station(codes={'R20'}, name={'zh': '唭哩岸'}),
  Station(codes={'R21'}, name={'zh': '奇岩'}),
  Station(codes={'R22'}, name={'zh': '北投'}),
  Station(codes={'R23'}, name={'zh': '復興崗'}),
  Station(codes={'R24'}, name={'zh': '忠義'}),
  Station(codes={'R25'}, name={'zh': '關渡'}),
  Station(codes={'R26'}, name={'zh': '竹圍'}),
  Station(codes={'R27'}, name={'zh': '紅樹林'}),
  Station(codes={'R28'}, name={'zh': '淡水'}),
  Station(codes={'R22A'}, name={'zh': '新北投'}),
  Station(codes={'G01'}, name={'zh': '新店'}),
  Station(codes={'G02'}, name={'zh': '新店區公所'}),
  Station(codes={'G03'}, name={'zh': '七張'}),
  Station(codes={'G04', 'Y07'}, name={'zh': '大坪林'}),
  Station(codes={'G05'}, name={'zh': '景美'}),
  Station(codes={'G06'}, name={'zh': '萬隆'}),
  Station(codes={'G07'}, name={'zh': '公館'}),
  Station(codes={'G08'}, name={'zh': '台電大樓'}),
  Station(codes={'G09', 'O05'}, name={'zh': '古亭'}),
  Station(codes={'G11'}, name={'zh': '小南門'}),
  Station(codes={'G12', 'BL11'}, name={'zh': '西門'}),
  Station(codes={'G13'}, name={'zh': '北門'}),
  Station(codes={'G15', 'O08'}, name={'zh': '松江南京'}),
  Station(codes={'G17'}, name={'zh': '台北小巨蛋'}),
  Station(codes={'G18'}, name={'zh': '南京三民'}),
  Station(codes={'G19'}, name={'zh': '松山'}),
  Station(codes={'G03A'}, name={'zh': '小碧潭'}),
  Station(codes={'O01'}, name={'zh': '南勢角'}),
  Station(codes={'O02', 'Y11'}, name={'zh': '景安'}),
  Station(codes={'O03'}, name={'zh': '永安市場'}),
  Station(codes={'O04'}, name={'zh': '頂溪'}),
  Station(codes={'O07', 'BL14'}, name={'zh': '忠孝新生'}),
  Station(codes={'O09'}, name={'zh': '行天宮'}),
  Station(codes={'O10'}, name={'zh': '中山國小'}),
  Station(codes={'O12'}, name={'zh': '大橋頭'}),
  Station(codes={'O13'}, name={'zh': '台北橋'}),
  Station(codes={'O14'}, name={'zh': '菜寮'}),
  Station(codes={'O15'}, name={'zh': '三重'}),
  Station(codes={'O16'}, name={'zh': '先嗇宮'}),
  Station(codes={'O17', 'Y18'}, name={'zh': '頭前庄'}),
  Station(codes={'O18'}, name={'zh': '新莊'}),
  Station(codes={'O19'}, name={'zh': '輔大'}),
  Station(codes={'O20'}, name={'zh': '丹鳳'}),
  Station(codes={'O21'}, name={'zh': '迴龍'}),
  Station(codes={'O50'}, name={'zh': '三重國小'}),
  Station(codes={'O51'}, name={'zh': '三和國中'}),
  Station(codes={'O52'}, name={'zh': '徐匯中學'}),
  Station(codes={'O53'}, name={'zh': '三民高中'}),
  Station(codes={'O54'}, name={'zh': '蘆洲'}),
  Station(codes={'BL01'}, name={'zh': '頂埔'}),
  Station(codes={'BL02'}, name={'zh': '永寧'}),
  Station(codes={'BL03'}, name={'zh': '土城'}),
  Station(codes={'BL04'}, name={'zh': '海山'}),
  Station(codes={'BL05'}, name={'zh': '亞東醫院'}),
  Station(codes={'BL06'}, name={'zh': '府中'}),
  Station(codes={'BL07'}, name={'zh': '板橋'}),
  Station(codes={'BL08'}, name={'zh': '新埔'}),
  Station(codes={'BL09'}, name={'zh': '江子翠'}),
  Station(codes={'BL10'}, name={'zh': '龍山寺'}),
  Station(codes={'BL13'}, name={'zh': '善導寺'}),
  Station(codes={'BL16'}, name={'zh': '忠孝敦化'}),
  Station(codes={'BL17'}, name={'zh': '國父紀念館'}),
  Station(codes={'BL18'}, name={'zh': '市政府'}),
  Station(codes={'BL19'}, name={'zh': '永春'}),
  Station(codes={'BL20'}, name={'zh': '後山埤'}),
  Station(codes={'BL21'}, name={'zh': '昆陽'}),
  Station(codes={'BL22'}, name={'zh': '南港'}),
  Station(codes={'Y08'}, name={'zh': '十四張'}),
  Station(codes={'Y09'}, name={'zh': '秀朗橋'}),
  Station(codes={'Y10'}, name={'zh': '景平'}),
  Station(codes={'Y12'}, name={'zh': '中和'}),
  Station(codes={'Y13'}, name={'zh': '橋和'}),
  Station(codes={'Y14'}, name={'zh': '中原'}),
  Station(codes={'Y15'}, name={'zh': '板新'}),
  Station(codes={'Y16'}, name={'zh': '板橋'}),
  Station(codes={'Y17'}, name={'zh': '新埔民生'}),
  Station(codes={'Y19'}, name={'zh': '幸福'}),
  Station(codes={'Y20'}, name={'zh': '新北產業園區'}),
}


def find_station(code: str) -> Station:
  return next(station for station in STATION_SET if code in station.codes)


class StationNode:
  def __init__(
    self,
    station: Station,
    code: str,
    next: 'StationNode | None' = None
  ) -> None:
    self.station = station
    self.code = code
    self.next = next


class Route:
  def __init__(self, name: str, arg: str) -> None:
    def __find_station(code):
      station = find_station(code)
      station.routes.append(self)
      return station

    self.name = name
    stations_code = arg.split('->')
    stations_linked_list = list(
      map(
        lambda x: StationNode(station=__find_station(x), code=x), stations_code
      )
    )
    for i, station_node in enumerate(stations_linked_list):
      if i < len(stations_linked_list) - 1:
        station_node.next = stations_linked_list[i + 1]
    self.heads = [stations_linked_list[0]]
    self.tail = stations_linked_list[-1]

  def is_in_route(self, code: str) -> bool:
    for head in self.heads:
      while head and code != head.code:
        head = head.next
      if head:
        return True
    return False

  def get_next_station_node(self, code: str) -> 'StationNode | None':
    for head in self.heads:
      while head and code != head.code:
        head = head.next
      if head:
        return head.next
    return None


def _init() -> 'tuple[list[dict[str, str | list[str]]], list[dict[str, str]]]':
  __Y16 = find_station('Y16')
  __Y17 = find_station('Y17')
  __BL07 = find_station('BL07')
  __BL08 = find_station('BL08')
  __Y16.out_of_station_transfers.append(__BL07)
  __BL07.out_of_station_transfers.append(__Y16)
  __Y17.out_of_station_transfers.append(__BL08)
  __BL08.out_of_station_transfers.append(__Y17)

  BR_routes = [
    Route(
      'BR01->BR24',
      'BR01->BR02->BR03->BR04->BR05->BR06->BR07->BR08->BR09->BR10->BR11->BR12->BR13->BR14->BR15->BR16->BR17->BR18->BR19->BR20->BR21->BR22->BR23->BR24'
    ),
    Route(
      'BR24->BR01',
      'BR24->BR23->BR22->BR21->BR20->BR19->BR18->BR17->BR16->BR15->BR14->BR13->BR12->BR11->BR10->BR09->BR08->BR07->BR06->BR05->BR04->BR03->BR02->BR01'
    )
  ]

  R_routes = [
    Route(
      'R02->R28',
      'R02->R03->R04->R05->R06->R07->R08->R09->R10->R11->R12->R13->R14->R15->R16->R17->R18->R19->R20->R21->R22->R23->R24->R25->R26->R27->R28'
    ),
    Route(
      'R28->R02',
      'R28->R27->R26->R25->R24->R23->R22->R21->R20->R19->R18->R17->R16->R15->R14->R13->R12->R11->R10->R09->R08->R07->R06->R05->R04->R03->R02'
    ),
    Route(
      'R05->R22',
      'R05->R06->R07->R08->R09->R10->R11->R12->R13->R14->R15->R16->R17->R18->R19->R20->R21->R22'
    ),
    Route(
      'R22->R05',
      'R22->R21->R20->R19->R18->R17->R16->R15->R14->R13->R12->R11->R10->R09->R08->R07->R06->R05'
    ),
    Route('R22->R22A', 'R22->R22A'),
    Route('R22A->R22', 'R22A->R22')
  ]

  G_routes = [
    Route(
      'G01->G19',
      'G01->G02->G03->G04->G05->G06->G07->G08->G09->G10->G11->G12->G13->G14->G15->G16->G17->G18->G19'
    ),
    Route(
      'G19->G01',
      'G19->G18->G17->G16->G15->G14->G13->G12->G11->G10->G09->G08->G07->G06->G05->G04->G03->G02->G01'
    ),
    Route(
      'G19->G08', 'G19->G18->G17->G16->G15->G14->G13->G12->G11->G10->G09->G08'
    ),
    Route('G03->G03A', 'G03->G03A'),
    Route('G03A->G03', 'G03A->G03')
  ]

  O_routes = [
    Route(
      'O01->O21',
      'O01->O02->O03->O04->O05->O06->O07->O08->O09->O10->O11->O12->O13->O14->O15->O16->O17->O18->O19->O20->O21'
    ),
    Route(
      'O01->O54',
      'O01->O02->O03->O04->O05->O06->O07->O08->O09->O10->O11->O12->O50->O51->O52->O53->O54'
    ),
    Route(
      'O21,O54->O01',
      'O21->O20->O19->O18->O17->O16->O15->O14->O13->O12->O11->O10->O09->O08->O07->O06->O05->O04->O03->O02->O01'
    )
  ]

  __O_temp = Route('', 'O54->O53->O52->O51->O50')  # ->O12
  __node = O_routes[2].heads[0]
  while __node.station != find_station('O12'):
    __node = __node.next
  __O_temp.tail.next = __node
  O_routes[2].heads.append(__O_temp.heads[0])
  for code in 'O54->O53->O52->O51->O50'.split('->'):
    station = find_station(code)
    station.routes.remove(__O_temp)
    station.routes.append(O_routes[2])
  del __O_temp

  BL_routes = [
    Route(
      'BL01->BL23',
      'BL01->BL02->BL03->BL04->BL05->BL06->BL07->BL08->BL09->BL10->BL11->BL12->BL13->BL14->BL15->BL16->BL17->BL18->BL19->BL20->BL21->BL22->BL23'
    ),
    Route(
      'BL05->BL21',
      'BL05->BL06->BL07->BL08->BL09->BL10->BL11->BL12->BL13->BL14->BL15->BL16->BL17->BL18->BL19->BL20->BL21'
    ),
    Route(
      'BL23->BL01',
      'BL23->BL22->BL21->BL20->BL19->BL18->BL17->BL16->BL15->BL14->BL13->BL12->BL11->BL10->BL09->BL08->BL07->BL06->BL05->BL04->BL03->BL02->BL01'
    ),
    Route(
      'BL23->BL05',
      'BL23->BL22->BL21->BL20->BL19->BL18->BL17->BL16->BL15->BL14->BL13->BL12->BL11->BL10->BL09->BL08->BL07->BL06->BL05'
    )
  ]

  Y_routes = [
    Route(
      'Y07->Y20',
      'Y07->Y08->Y09->Y10->Y11->Y12->Y13->Y14->Y15->Y16->Y17->Y18->Y19->Y20'
    ),
    Route(
      'Y20->Y07',
      'Y20->Y19->Y18->Y17->Y16->Y15->Y14->Y13->Y12->Y11->Y10->Y09->Y08->Y07'
    )
  ]

  states = [{'name': 'home', 'on_enter': ['go_home']}]
  transitions = []

  for station in STATION_SET:
    station_str = str(station)
    states.append({'name': station_str, 'on_enter': ['go_to_station']})
    transitions.append(
      {
        'trigger': station_str,
        'source': 'home',
        'dest': station_str
      }
    )
    transitions.append(
      {
        'trigger': 'home',
        'source': station_str,
        'dest': 'home'
      }
    )
    for route in station.routes:
      tail_code = next(
        code for code in route.tail.station.codes if route.is_in_route(code)
      )
      tail_str = route.tail.station.name['zh'] + '(' + tail_code + ')'
      station_current_code = next(
        code for code in station.codes if route.is_in_route(code)
      )
      station_current_str = station.name['zh'] + '(' + station_current_code + ')'
      car_name = station_current_str + '->' + tail_str
      is_head = station in map(lambda x: x.station, route.heads)
      if not is_head:
        states.append({'name': car_name, 'on_enter': ['get_on_car']})
        transitions.append(
          {
            'trigger': 'get_off',
            'source': car_name,
            'dest': station_str
          }
        )
      next_station_node = route.get_next_station_node(station_current_code)
      if next_station_node:
        next_station_current_code = next_station_node.code
        next_station_current_str = next_station_node.station.name[
          'zh'] + '(' + next_station_current_code + ')'
        next_car_name = next_station_current_str + '->' + tail_str
        transitions.append(
          {
            'trigger': tail_code,
            'source': station_str,
            'dest': next_car_name
          }
        )
        if not is_head:
          transitions.append(
            {
              'trigger': 'continue',
              'source': car_name,
              'dest': next_car_name
            }
          )
    for out_of_station_transfer in station.out_of_station_transfers:
      transitions.append(
        {
          'trigger': str(out_of_station_transfer),
          'source': station_str,
          'dest': str(out_of_station_transfer)
        }
      )

  return states, transitions


class Model:
  __SPECIAL_INFOS = {
    'BR01': '往動物園旅客請由一號出口出站；往貓空纜車旅客請由二號出口出站',
    'BR09': '轉乘淡水信義線，請在本站換車',
    'BR10': '轉乘板南線，請在本站換車',
    'BR11': '轉乘松山新店線，請在本站換車',
    'BR24': '轉乘板南線，請在本站換車',
    'R05':
      {
        'R02': '轉乘文湖線，請在本站換車',
        'R05': '本區間車終點站大安站，到站後不再提供載客服務。轉乘文湖線及往象山的旅客，請在本站換車',
      },
    'R07': '轉乘中和新蘆線，請在本站換車。換車時請勿奔跑',
    'R08': '轉乘松山新店線，請在本站換車。換車時請勿奔跑',
    'R10': '轉乘板南線、臺鐵、高鐵、桃園機場捷運，請在本站換車。下車時請注意間隙',
    'R11': '轉乘松山新店線，請在本站換車',
    'R13': '轉乘中和新蘆線，請在本站換車',
    'R22':
      {
        'R02': '往新北投的旅客，請在本站換車',
        'R22': {
          'R21': '往新北投及淡水方向的旅客，請在本站換車',
          'R22A': '轉乘淡水信義線，請在本站換車'
        },
        'R28': '往新北投的旅客，請在本站換車'
      },
    'R27': '轉乘淡海輕軌，請在本站換車',
    'G03':
      {
        'G01': '往小碧潭站的旅客，請在本站換車。往碧潭風景區的旅客，請到新店站下車',
        'G03': '本列車到站後不再提供載客服務，轉乘松山新店線，請在本站換車',
        'G19': '往小碧潭站的旅客，請在本站換車'
      },
    'G04': '轉乘環狀線，請在本站換車',
    'G08': {
      'G08': '本區間車終點站台電大樓站，到站後不再提供載客服務，往新店方向的旅客請在本站換車'
    },
    'G09': '轉乘中和新蘆線，請在本站換車。換車時請勿奔跑',
    'G10': '轉乘淡水信義線，請在本站換車。換車時請勿奔跑',
    'G12': '轉乘板南線，請在本站換車。換車時請勿奔跑',
    'G13': '轉乘桃園機場捷運，請在本站換車',
    'G14': '轉乘淡水信義線，請在本站換車',
    'G15': '轉乘中和新蘆線，請在本站換車',
    'G16': '轉乘文湖線，請在本站換車',
    'G19': '轉乘臺鐵，請在本站換車',
    'O02': '轉乘環狀線，請在本站換車',
    'O05': '轉乘松山新店線，請在本站換車。換車時請勿奔跑',
    'O06': '轉乘淡水信義線，請在本站換車。換車時請勿奔跑',
    'O07': '轉乘板南線，請在本站換車',
    'O08': '轉乘松山新店線，請在本站換車',
    'O11': '轉乘淡水信義線，請在本站換車',
    'O12': {
      'O21': '往蘆洲方向的旅客，請站本站換車',
      'O54': '往迴龍方向的旅客，請在本站換車'
    },
    'O15': '轉乘桃園機場捷運，請在本站換車',
    'O17': '轉乘環狀線，請在本站換車',
    'BL05': {
      'BL05': '本列車到站後不再提供載客服務，往頂埔方向的旅客，請在本站換車'
    },
    'BL07': '轉乘環狀線、臺鐵、高鐵，請在本站換車',
    'BL08': '轉乘環狀線，請在本站換車',
    'BL11': '轉乘松山新店線，請在本站換車。換車時請勿奔跑',
    'BL12': '轉乘淡水信義線、臺鐵、高鐵、桃園機場捷運，請在本站換車',
    'BL14': '轉乘中和新蘆線，請在本站換車',
    'BL15': '轉乘文湖線，請在本站換車',
    'BL21': {
      'BL21': '本列車到站後不再提供載客服務，往南港展覽館方向的旅客請在本站換車'
    },
    'BL22': '轉乘臺鐵、高鐵，請在本站換車',
    'BL23': '轉乘文湖線，請在本站換車',
    'Y07': '轉乘松山新店線，請在本站換車',
    'Y11': '轉乘中和新蘆線，請在本站換車',
    'Y16': '轉乘板南線、臺鐵、高鐵，請在本站換車',
    'Y17': '轉乘板南線，請在本站換車',
    'Y18': '轉乘中和新蘆線，請在本站換車',
    'Y20': '轉乘桃園機場捷運，請在本站換車'
  }

  def __init__(self) -> None:
    self.__info_str = '您好'
    self.__previous_state = None

  @property
  def info_str(self) -> str:
    return self.__info_str

  def before_state_change(self) -> None:
    self.__info_str = ''
    self.__previous_state = self.state

  def go_home(self) -> None:
    self.__info_str += '歡迎回家'

  def go_to_station(self) -> None:
    name = find_station(self.state.split('(')[1].split(')')[0].split(',')[0]
                       ).name['zh']
    if name[-1] != '站':
      name += '站'
    self.__info_str += '歡迎來到' + name

  def get_on_car(self) -> None:
    from_code = self.state.split('->')[0].split('(')[1].split(')')[0]
    terminal_code = self.state.split('->')[1].split('(')[1].split(')')[0]
    if from_code in Model.__SPECIAL_INFOS:
      content = Model.__SPECIAL_INFOS[from_code]
      if type(content) is str:
        self.__info_str += content
      else:
        if terminal_code in content:
          content = content[terminal_code]
          if type(content) is str:
            self.__info_str += content
          else:
            previous_code = self.__previous_state.split('(')[1].split(')')[0]
            if previous_code in content:
              self.__info_str += content[previous_code]


class TaipeiMRTMachine(GraphMachine):
  __STATES, __TRANSITIONS = _init()

  __KWARGS = {
    'states': __STATES,
    'transitions': __TRANSITIONS,
    'initial': 'home',
    'auto_transitions': False,
    'before_state_change': 'before_state_change'
  }

  def __init__(self) -> None:
    self.m = Model()
    kwargs = dict(TaipeiMRTMachine.__KWARGS)
    kwargs.update(model=self.m)
    super().__init__(**kwargs)

  def trigger(self, trigger_name: str):
    return self.m.trigger(trigger_name)

  @property
  def state(self) -> str:
    return self.m.state

  @property
  def info_str(self) -> str:
    return self.m.info_str

  @property
  def options(self) -> list:
    return self.get_triggers(self.m.state)


if __name__ == '__main__':
  import random

  for _ in range(1):
    machine = TaipeiMRTMachine()
    # machine.trigger('中正紀念堂(G10, R08)')
    # machine.m.get_graph().draw('fsm.svg', prog='fdp')
    while True:
      while True:
        choice = random.choice(machine.get_triggers(machine.state))
        if choice != 'home':
          break
      print('\t', choice)
      machine.trigger(choice)
      print(machine.state)
      if machine.state == '淡水(R28)':
        break
    # triggers = [
    #   '中正紀念堂(G10, R08)',
    #   'R02',
    #   'get_off',
    # ]
    # for trigger in triggers:
    #   machine.trigger(trigger)
    #   print(machine.state, end='')
    #   if machine.info_str:
    #     print(':', machine.info_str)
    #   else:
    #     print()
