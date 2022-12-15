from cmath import phase
from distutils.log import debug
from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from django.conf import settings
from django.core.cache import cache
import random


class MultiPlayer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = None
        # self.phase = []

        for i in range(1000):
            name = "room-%d" % (i)
            if not cache.has_key(name) or len(cache.get(name)) < 2:
                self.room_name = name
                print('name='+name)
                break

        if not self.room_name:
            return

        await self.accept()

        if not cache.has_key(self.room_name):
            cache.set(self.room_name, [], 3600)  # 有效期1小时

        # 房间中已有玩家信息
        # for player in cache.get(self.room_name):
        #     await self.send(text_data=json.dumps({
        #         'eventname': "create_player",
        #         'username': player['username'],
        #     }))

        await self.channel_layer.group_add(self.room_name, self.channel_name)

    async def disconnect(self, close_code):
        print('disconnect')
        cache.delete(self.room_name)
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # 接收数据
    async def receive(self, text_data):
        # print('receive '+text_data)
        # print(self.message_count)
        data = json.loads(text_data)
        event = data['eventname']
        if event == "create_player":
            await self.create_player(data)
        elif event == "set_result" or event == "card_panel_result":
            await self.set_result(data)
        elif event == "execute_phase":
            await self.execute_phase(data)
        elif event == "shuffle":
            await self.shuffle(data)
        elif event == "ban_pick_result":
            await self.ban_pick_result(data)
        elif event == "self_pick_result":
            await self.self_pick_result(data)
        elif event == "surrender":
            await self.surrender(data)

    async def group_send_event(self, data):
        await self.send(text_data=json.dumps(data))

    # 创建玩家
    async def create_player(self, data):
        # print("create_player")
        players = cache.get(self.room_name)
        players.append({
            'username': data['username'],
            'message': 0
        })
        cache.set(self.room_name, players, 3600)  # 有效期1小时
        # await self.channel_layer.group_send(
        #     self.room_name,
        #     {
        #         'type': 'group_send_event',
        #         'eventname': 'create_player',
        #         'username': data['username'],
        #     }
        # )

        if len(cache.get(self.room_name)) == 2:
            await self.start_game(data)

    # async def remove_player(self, data):
    #     cache.get(self.room_name).clear()
        # for i in players:
        #     if i['username'] == data['username']:
        #         players.remove(i)
        #         break

    # 开始游戏
    async def start_game(self, data):
        players = []
        for player in cache.get(self.room_name):
            players.append(player['username'])
        random.shuffle(players)
        players.append(players[1])
        players.append(players[0])

        print('start game')

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'group_send_event',
                'eventname': 'start_game',
                'players': players,
                'generals': random.sample(range(0, 14), 12)
            }
        )

    # message_count = 0

    async def set_result(self, data):
        # if data['id'] != self.message_count + 1:
        #     return
        # self.message_count += 1

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'group_send_event',
                'eventname': data['eventname'],
                'id': data['id'],
                'result': data['result'],
                'cards': data['cards'],
                'dests': data['dests'],
                'src': data['src'],
                'skill': data['skill'],
                'other': data['other']
            }
        )

    async def ban_pick_result(self, data):
        # if data['id'] != self.message_count + 1:
        #     return
        # self.message_count += 1

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'group_send_event',
                'eventname': data['eventname'],
                'id': data['id'],
                'general': data['general']
            }
        )

    async def self_pick_result(self, data):
        # if data['id'] != self.message_count + 1:
        #     return
        # self.message_count += 1

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'group_send_event',
                'eventname': data['eventname'],
                'id': data['id'],
                'team': data['team'],
                'general0': data['general0'],
                'general1': data['general1']
            }
        )

    async def surrender(self, data):
        # if data['id'] != self.message_count + 1:
        #     return
        # self.message_count += 1

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'group_send_event',
                'eventname': data['eventname'],
                'team': data['team'],
            }
        )

    async def execute_phase(self, data):
        # if data['id'] != self.message_count + 1:
        #     return
        # self.message_count += 1
        # self.phase.append(data)
        # print('phase.len==',len(self.phase))

        # if len(self.phase) >= 2:
        # self.phase.clear()
        players = cache.get(self.room_name)
        for i in players:
            if i['username'] == data['username']:
                i['message'] += 1
            else:
                print(data['username'])
            print(i['message'])
        cache.set(self.room_name, players, 3600)

        for i in cache.get(self.room_name):
            if i['message'] == 0:
                print('return')
                return

        for i in cache.get(self.room_name):
            i['message'] = 0
        cache.set(self.room_name, players, 3600)
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'group_send_event',
                'eventname': 'execute_phase',
                'id': data['id'],
                'username': data['username'],
                'phase': data['phase']
            }
        )

    async def shuffle(self, data):
        # if data['id'] != self.message_count + 1:
        #     print(self.message_count)
        #     return
        # self.message_count += 1

        random.shuffle(data['cards'])
        print('shuffle')

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'group_send_event',
                'eventname': 'shuffle',
                'id': data['id'],
                'cards': data['cards']
            }
        )
