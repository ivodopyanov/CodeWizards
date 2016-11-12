import random, math

from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World
from model.LaneType import LaneType
from model.Faction import Faction
from model.BuildingType import BuildingType


GRAPH = {}
def build_waypoint_graph():
        base1N = [(300,3400), (400,3400), (500,3400)]
        base1E = [(600, 3500), (600,3600), (600,3700)]
        base1S = [(500,3800), (400,3800), (300,3800)]
        base1W = [(200, 3700), (200, 3600), (200, 3500)]

        base1NW = (200, 3400)
        base1NE = (600, 3400)
        base1SE = (600, 3800)
        base1SW = (200, 3800)

        GRAPH[base1NW] = [base1W[-1], base1N[0]]
        GRAPH[base1NE] = [base1N[-1], base1E[0]]
        GRAPH[base1SE] = [base1E[-1], base1S[0]]
        GRAPH[base1SW] = [base1S[-1], base1W[0]]

        GRAPH[base1N[0]] = [base1NW, base1N[1]]
        GRAPH[base1N[1]] = [base1N[0], base1N[2]]
        GRAPH[base1N[2]] = [base1N[1], base1NE]
        GRAPH[base1E[0]] = [base1NE, base1E[1]]
        GRAPH[base1E[1]] = [base1E[0], base1E[2]]
        GRAPH[base1E[2]] = [base1SE, base1E[1]]
        GRAPH[base1S[0]] = [base1SE, base1S[1]]
        GRAPH[base1S[1]] = [base1S[0], base1S[2]]
        GRAPH[base1S[2]] = [base1SW, base1S[1]]
        GRAPH[base1W[0]] = [base1SW, base1W[1]]
        GRAPH[base1W[1]] = [base1W[0], base1W[2]]
        GRAPH[base1W[2]] = [base1NW, base1W[1]]

        base2N = [(3500, 200), (3600, 200), (3700, 200)]
        base2E = [(3800, 300), (3800, 400), (3800, 500)]
        base2S = [(3700, 600), (3600, 600), (3500, 600)]
        base2W = [(3400, 500), (3400, 400), (3400, 300)]

        base2NW = (3400, 200)
        base2SW = (3400, 600)
        base2SE = (3800, 600)
        base2NE = (3800, 200)

        GRAPH[base2NW] = [base2W[-1], base2N[0]]
        GRAPH[base2NE] = [base2N[-1], base2E[0]]
        GRAPH[base2SE] = [base2E[-1], base2S[0]]
        GRAPH[base2SW] = [base2S[-1], base2W[0]]

        GRAPH[base2N[0]] = [base2NW, base2N[1]]
        GRAPH[base2N[1]] = [base2N[0], base2N[2]]
        GRAPH[base2N[2]] = [base2N[1], base2NE]
        GRAPH[base2E[0]] = [base2NE, base2E[1]]
        GRAPH[base2E[1]] = [base2E[0], base2E[2]]
        GRAPH[base2E[2]] = [base2SE, base2E[1]]
        GRAPH[base2S[0]] = [base2SE, base2S[1]]
        GRAPH[base2S[1]] = [base2S[0], base2S[2]]
        GRAPH[base2S[2]] = [base2SW, base2S[1]]
        GRAPH[base2W[0]] = [base2SW, base2W[1]]
        GRAPH[base2W[1]] = [base2W[0], base2W[2]]
        GRAPH[base2W[2]] = [base2NW, base2W[1]]


        #3200-400
        west_lane = []
        for y in range(3200, 300,-100):
            west_lane.append((200, y))

        north_lane = []
        #400-3300
        for x in range(400, 3400, 100):
            north_lane.append((x, 200))

        #700-3600
        east_lane = []
        for y in range(700, 3700, 100):
            east_lane.append((3800, y))

        #3600-700
        south_lane = []
        for x in range(3600, 600, -100):
            south_lane.append((x, 3800))


        GRAPH[base1NW].append(west_lane[0])
        GRAPH[base2NW].append(north_lane[-1])
        GRAPH[base2SE].append(east_lane[0])
        GRAPH[base1SE].append(south_lane[-1])

        GRAPH[west_lane[0]] = [base1NW, west_lane[1]]
        for i in range(1, len(west_lane)-1):
            GRAPH[west_lane[i]] = [west_lane[i-1], west_lane[i+1]]
        GRAPH[west_lane[-1]] = [west_lane[-2], north_lane[0]]
        GRAPH[north_lane[0]] = [west_lane[-1], north_lane[1]]
        for i in range(1, len(north_lane)-1):
            GRAPH[north_lane[i]] = [north_lane[i-1], north_lane[i+1]]
        GRAPH[north_lane[-1]] = [north_lane[-2], base2NW]
        GRAPH[east_lane[0]] = [base2SE, east_lane[1]]
        for i in range(1, len(east_lane)-1):
            GRAPH[east_lane[i]] = [east_lane[i-1], east_lane[i+1]]
        GRAPH[east_lane[-1]] = [east_lane[-2], south_lane[0]]
        GRAPH[south_lane[0]] = [east_lane[-1], south_lane[1]]
        for i in range(1, len(south_lane)-1):
            GRAPH[south_lane[i]] = [south_lane[i-1], south_lane[i+1]]
        GRAPH[south_lane[-1]] = [south_lane[-2], base1SE]


        center = (2000,2000)
        NW_to_center_lane = []
        NE_to_center_lane = []
        SE_to_center_lane = []
        SW_to_center_lane = []
        for shift in range(400,1800,100):
            NW_to_center_lane.append((shift, shift))
            NE_to_center_lane.append((4000-shift, shift))
            SE_to_center_lane.append((4000-shift, 4000-shift))
            SW_to_center_lane.append((shift, 4000-shift))
        del SW_to_center_lane[0]
        del NE_to_center_lane[0]

        GRAPH[west_lane[-1]].append(NW_to_center_lane[0])
        GRAPH[north_lane[0]].append(NW_to_center_lane[0])

        GRAPH[base2SW].append(NE_to_center_lane[0])

        GRAPH[east_lane[-1]].append(SE_to_center_lane[0])
        GRAPH[south_lane[0]].append(SE_to_center_lane[0])

        GRAPH[base1NE].append(SW_to_center_lane[0])

        GRAPH[NW_to_center_lane[0]] = [west_lane[-1], north_lane[0], NW_to_center_lane[1]]
        GRAPH[NE_to_center_lane[0]] = [base2SW, NE_to_center_lane[1]]
        GRAPH[SE_to_center_lane[0]] = [east_lane[-1], south_lane[0], SE_to_center_lane[1]]
        GRAPH[SW_to_center_lane[0]] = [base1NE, SW_to_center_lane[1]]
        
        for i in range(1, len(NW_to_center_lane)-1):
            GRAPH[NW_to_center_lane[i]] = [NW_to_center_lane[i-1], NW_to_center_lane[i+1]]
        GRAPH[NW_to_center_lane[-1]] = [NW_to_center_lane[-2], center]
        
        for i in range(1, len(NE_to_center_lane)-1):
            GRAPH[NE_to_center_lane[i]] = [NE_to_center_lane[i-1], NE_to_center_lane[i+1]]
        GRAPH[NE_to_center_lane[-1]] = [NE_to_center_lane[-2], center]
        
        for i in range(1, len(SE_to_center_lane)-1):
            GRAPH[SE_to_center_lane[i]] = [SE_to_center_lane[i-1], SE_to_center_lane[i+1]]
        GRAPH[SE_to_center_lane[-1]] = [SE_to_center_lane[-2], center]
        
        for i in range(1, len(SW_to_center_lane)-1):
            GRAPH[SW_to_center_lane[i]] = [SW_to_center_lane[i-1], SW_to_center_lane[i+1]]
        GRAPH[SW_to_center_lane[-1]] = [SW_to_center_lane[-2], center]
        
        GRAPH[center] = [NW_to_center_lane[-1], NE_to_center_lane[-1], SE_to_center_lane[-1], SW_to_center_lane[-1]]


build_waypoint_graph()


def pathfinder_macro(start, goal):
    open_nodes = [{'node': start, 'dist':0}]
    closed_nodes = set()
    parents = {}

    while len(open_nodes) > 0:
        open_nodes.sort(key=lambda st:st['dist']+math.hypot(st['node'][0]-goal[0], st['node'][1]-goal[1]))
        st = open_nodes.pop(0)
        node = st['node']
        dist = st['dist']
        closed_nodes.add(node)
        for next_node in GRAPH[node]:
            if next_node == goal:
                path = [next_node, node]
                back_node = node
                while back_node in parents:
                    path.append(parents[back_node])
                    back_node = parents[back_node]
                return path
            if next_node not in closed_nodes:

                open_nodes.append({'node': next_node, 'dist': dist+math.hypot(next_node[0] - node[0], next_node[1] - node[1])})
                parents[next_node] = node
    return None

MICRO_X_DISP = 5
MICRO_Y_DISP = 5
def pathfinder_micro(me: Wizard, obstacles, start, goal):
    open_nodes = [{'node': start, 'dist':0}]
    closed_nodes = set()
    parents = {}

    distance_to_succeed = 10
    for obstacle in obstacles:
        if math.hypot(goal[0] - obstacle['x'], goal[1] - obstacle['y']) <= obstacle['radius'] + me.radius + 5:
            goal = (obstacle['x'], obstacle['y'])
            distance_to_succeed = obstacle['radius'] + me.radius + 5
            break
    if math.hypot(start[0]-goal[0], start[1]-goal[1]) <= distance_to_succeed:
        return [start, goal]

    goal = (int(goal[0]), int(goal[1]))


    while len(open_nodes) > 0:
        open_nodes.sort(key=lambda st:st['dist']+math.hypot(st['node'][0]-goal[0], st['node'][1]-goal[1]))
        st = open_nodes.pop(0)
        node = st['node']
        dist = st['dist']
        closed_nodes.add(node)
        candidates =  [ [1]*(2*MICRO_X_DISP+1) for _ in range(2*MICRO_Y_DISP+1)]

        for obstacle in obstacles:
            if math.hypot(node[0] - obstacle['x'], node[1] - obstacle['y']) > obstacle['radius'] + me.radius + 5:
                continue
            for y in range(2*MICRO_Y_DISP + 1):
                for x in range(2*MICRO_X_DISP + 1):
                    x_pos = node[0] + x - MICRO_X_DISP
                    y_pos = node[1] + y - MICRO_Y_DISP
                    if x_pos < 0 or x_pos > 4000 or y_pos < 0 or y_pos > 4000:
                        candidates[y][x] = 0
                        continue
                    if math.hypot(x_pos-obstacle['x'], y_pos-obstacle['y']) < me.radius+obstacle['radius']:
                        candidates[y][x] = 0

        #вырезаем кандидаты внутри, если будем проверять их соседние (те, которые дальше от центра)
        for y in range(MICRO_Y_DISP,0,-1):
            for x in range(MICRO_X_DISP,0,-1):
                if candidates[y-1][x] == 1 or candidates[y][x-1] == 1 or candidates[y-1][x-1] == 1:
                    candidates[y][x] = 0
            for x in range(MICRO_X_DISP+1,2*MICRO_X_DISP,1):
                if candidates[y-1][x] == 1 or candidates[y][x+1] == 1 or candidates[y-1][x+1] == 1:
                    candidates[y][x] = 0

            if candidates[y-1][0] == 1:
                candidates[y][0] = 0
            if candidates[y-1][2*MICRO_X_DISP] == 1:
                candidates[y][2*MICRO_X_DISP] = 0
        for y in range(MICRO_Y_DISP+1,2*MICRO_Y_DISP,1):
            for x in range(MICRO_X_DISP,0,-1):
                if candidates[y+1][x] == 1 or candidates[y][x-1] == 1 or candidates[y+1][x-1] == 1:
                    candidates[y][x] = 0
            for x in range(MICRO_X_DISP+1,2*MICRO_X_DISP,1):
                if candidates[y+1][x] == 1 or candidates[y][x+1] == 1 or candidates[y+1][x+1] == 1:
                    candidates[y][x] = 0
            if candidates[y+1][0] == 1:
                candidates[y][0] = 0
            if candidates[y+1][2*MICRO_X_DISP] == 1:
                candidates[y][2*MICRO_X_DISP] = 0

        for y in range(MICRO_Y_DISP,0,-1):
            if candidates[y-1][0] == 1:
                candidates[y][0] = 0
            if candidates[y-1][2*MICRO_X_DISP] == 1:
                candidates[y][2*MICRO_X_DISP] = 0
        for y in range(MICRO_Y_DISP+1,2*MICRO_Y_DISP,1):
            if candidates[y+1][0] == 1:
                candidates[y][0] = 0
            if candidates[y+1][2*MICRO_X_DISP] == 1:
                candidates[y][2*MICRO_X_DISP] = 0
        for x in range(MICRO_X_DISP,0,-1):
            if candidates[0][x-1] == 1:
                candidates[0][x] = 0
            if candidates[2*MICRO_Y_DISP][x-1] == 1:
                candidates[2*MICRO_Y_DISP][x] = 0
        for x in range(MICRO_X_DISP+1,2*MICRO_X_DISP,1):
            if candidates[0][x+1] == 1:
                candidates[0][x] = 0
            if candidates[2*MICRO_Y_DISP][x+1] == 1:
                candidates[2*MICRO_Y_DISP][x] = 0



        for y in range(2*MICRO_Y_DISP+1):
            for x in range(2*MICRO_X_DISP+1):
                if candidates[y][x] == 0:
                    continue
                next_node = (node[0] + x - MICRO_X_DISP, node[1] + y - MICRO_Y_DISP)
                if math.hypot(next_node[0]-goal[0], next_node[1]-goal[1]) <= distance_to_succeed:
                    path = [next_node, node]
                    back_node = node
                    while back_node in parents:
                        path.append(parents[back_node])
                        back_node = parents[back_node]
                    return path
                if next_node not in closed_nodes:

                    open_nodes.append({'node': next_node, 'dist': dist+1})
                    parents[next_node] = node
    return None


#find_path((200, 3400), (3400, 600))
LANE_NAMES = ["top_lane", "center_lane", "bottom_lane"]
WAYPOINTS = {"top_lane": (600,600),
             "center_lane": (2000,2000),
             "bottom_lane": (3400,3400),
             "base1": (200,3800),
             "base2": (3800,200),
             "bonus1": (1200,1200),
             "bonus2": (2800, 2800)}

SHIFT = 200
RETREAT_RADIUS = 100
RETREAT_THREAT_RADIUS = 300

START_MODE = 0
GO_TO_LANE = 1
GO_TO_ENEMY_BASE = 2
GO_TO_MY_BASE = 3


UNIT_WIZARD = 0
UNIT_MINION = 1
UNIT_BUILDING = 2

OBSTACLE_BUILDING = 0
OBSTACLE_TREE = 1
OBSTACLE_WIZARD = 2
OBSTACLE_MINION = 3
GROUPABLE_OBSTACLES = [OBSTACLE_BUILDING, OBSTACLE_TREE]

def sign(x):
    if x==0:
        return 0
    else:
        return abs(x)/x

class MyStrategy:

    def __init__(self):
        self.mode = START_MODE
        self.last_coors = None
        self.current_goal = None
        self.fightning = False
        self.return_to_track = False
        self.wait_for_bonus = False
        self.path_macro = []
        self.path_micro = []

    def find_enemies_nearby(self, me:Wizard, world:World):
        result = []

        for wizard in world.wizards:
            if wizard.faction != me.faction and wizard.get_distance_to_unit(me) < me.cast_range*1.2:
                result.append({"dist": wizard.get_distance_to_unit(me), "unit": wizard, "type": UNIT_WIZARD})
        for minion in world.minions:
            if minion.faction != me.faction and minion.faction != Faction.NEUTRAL and minion.get_distance_to_unit(me) < me.cast_range*1.2:
                result.append({"dist": minion.get_distance_to_unit(me), "unit":minion, "type":UNIT_MINION})
        for building in world.buildings:
            if building.faction != me.faction and building.get_distance_to_unit(me) < me.cast_range*1.2:
                result.append({"dist": building.get_distance_to_unit(me), "unit": building, "type":UNIT_BUILDING})
        result.sort(key=lambda data: data["dist"])
        return result

    def find_nearest_ally_to_enemy(self, me, enemy, world: World, game: Game):
        dist = 9999
        unit = None
        type = -1

        for wizard in world.wizards:
            if wizard.x == me.x and wizard.y == me.y:
                continue
            if wizard.faction != enemy.faction and wizard.get_distance_to_unit(enemy) < dist and wizard.life > game.magic_missile_direct_damage:
                dist = wizard.get_distance_to_unit(enemy)
                unit = wizard
                type = UNIT_WIZARD
        for minion in world.minions:
            if minion.faction != enemy.faction and minion.faction != Faction.NEUTRAL and minion.get_distance_to_unit(enemy) < dist and minion.life > game.magic_missile_direct_damage:
                dist = minion.get_distance_to_unit(enemy)
                unit = minion
                type = UNIT_MINION
        for building in world.buildings:
            if building.faction != enemy.faction and building.get_distance_to_unit(enemy) < dist and building.life > game.magic_missile_direct_damage:
                dist = building.get_distance_to_unit(enemy)
                unit = building
                type = UNIT_BUILDING
        result = {"unit": unit, "dist": dist, "type":type}
        return result

    def scan_aroud(self, me, world, game):
        threats = []
        allies = []

        for wizard in world.wizards:
            if wizard.get_distance_to_unit(me) < me.cast_range*1.2 and wizard.faction != me.faction:
                    threats.append(wizard)
            if wizard.faction == me.faction and wizard.get_distance_to_unit(me) < me.cast_range and abs(me.get_angle_to_unit(wizard)) < math.pi/3 and (wizard.x!=me.x or wizard.y!=me.y):
                    allies.append(wizard)
        for minion in world.minions:
            if minion.get_distance_to_unit(me) < me.cast_range and minion.faction != me.faction and minion.faction != Faction.NEUTRAL:
                    threats.append(minion)
            if minion.faction == me.faction and minion.get_distance_to_unit(me) < me.cast_range and abs(me.get_angle_to_unit(minion)) < math.pi/4:
                    allies.append(minion)
        for building in world.buildings:
            if building.get_distance_to_unit(me) < me.cast_range and building.faction != me.faction and building.faction != Faction.NEUTRAL:
                    threats.append(building)
            if building.faction == me.faction and building.get_distance_to_unit(me) < me.cast_range and abs(me.get_angle_to_unit(building)) < math.pi/4:
                    allies.append(building)

        direct_threats = []
        for threat in threats:
            threat_target = self.find_nearest_ally_to_enemy(me, threat, world, game)
            if threat_target["unit"] is None or threat_target["dist"] > me.get_distance_to_unit(threat) + 10:
                direct_threats.append(threat)
        return threats, direct_threats, allies



    def calc_retreat_angle(self, me, threats):
        total_angle = 0
        for threat in threats:
            total_angle += me.get_angle_to_unit(threat)
        return total_angle


    def find_nearest_obstacle_in_front(self, me:Wizard, world:World):
        distance = 9999
        object = None
        type = None
        for building in world.buildings:
            angle = me.get_angle_to_unit(building)
            d = me.get_distance_to_unit(building)
            if abs(angle) < math.pi/2 and d < distance:
                object = building
                distance = d - building.radius
                type = OBSTACLE_BUILDING
        for tree in world.trees:
            angle = me.get_angle_to_unit(tree)
            d = me.get_distance_to_unit(tree)
            if abs(angle) < math.pi/2  and d < distance:
                object = tree
                distance = d - tree.radius
                type = OBSTACLE_TREE
        for wizard in world.wizards:
            if wizard.faction == me.faction and (wizard.x!=me.x or wizard.y!=me.y):
                angle = me.get_angle_to_unit(wizard)
                d = me.get_distance_to_unit(wizard)
                if abs(angle) < math.pi/2 and d < distance:
                    object = wizard
                    distance = d - wizard.radius
                    type = OBSTACLE_WIZARD
        for minion in world.minions:
            if minion.faction == me.faction or minion.faction==Faction.NEUTRAL:
                angle = me.get_angle_to_unit(minion)
                d = me.get_distance_to_unit(minion)
                if abs(angle) < math.pi/2 and d < distance:
                    object = minion
                    distance = d - minion.radius
                    type = OBSTACLE_MINION

        if distance < me.radius + 40:
            return object, type
        return None, None

    def build_obstacles_list(self, me: Wizard, world: World):
        #Получили список всех препятствий на карте
        obstacles = []
        for building in world.buildings:
            obstacles.append({"x": building.x, "y": building.y, "radius": building.radius, "type": OBSTACLE_BUILDING})
        for tree in world.trees:
            obstacles.append({"x": tree.x, "y": tree.y, "radius": tree.radius, "type": OBSTACLE_TREE})
        for wizard in world.wizards:
            if wizard.x != me.x and wizard.y != me.y:
                obstacles.append({"x": wizard.x, "y": wizard.y, "radius": wizard.radius, "type": OBSTACLE_WIZARD})
        for minion in world.minions:
            obstacles.append({"x": minion.x, "y": minion.y, "radius": minion.radius, "type": OBSTACLE_MINION})
        return obstacles



    def find_nearest_obstacle_in_behind(self, me:Wizard, world:World):
        distance = 9999
        object = None
        type = None
        for building in world.buildings:
            angle = me.get_angle_to_unit(building)
            d = me.get_distance_to_unit(building)
            if abs(angle) > math.pi/2 and d < distance:
                object = building
                distance = d - building.radius
                type = OBSTACLE_BUILDING
        for tree in world.trees:
            angle = me.get_angle_to_unit(tree)
            d = me.get_distance_to_unit(tree)
            if abs(angle) > math.pi/2 and d < distance:
                object = tree
                distance = d - tree.radius
                type = OBSTACLE_TREE
        for wizard in world.wizards:
            if wizard.faction == me.faction and (wizard.x!=me.x or wizard.y!=me.y):
                angle = me.get_angle_to_unit(wizard)
                d = me.get_distance_to_unit(wizard)
                if abs(angle) > math.pi/2 and d < distance:
                    object = wizard
                    distance = d - wizard.radius
                    type = OBSTACLE_WIZARD
        for minion in world.minions:
            if minion.faction == me.faction or minion.faction==Faction.NEUTRAL:
                angle = me.get_angle_to_unit(minion)
                d = me.get_distance_to_unit(minion)
                if abs(angle) > math.pi/2 and d < distance:
                    object = minion
                    distance = d - minion.radius
                    type = OBSTACLE_MINION
        if distance < me.radius + 10:
            return object, type
        return None, None

    def select_unit_for_attack(self, enemies, damage):
        if len(enemies) == 0:
            return None
        enemies_by_life = sorted(enemies, key=lambda enemy: enemy["unit"].life)
        target = enemies_by_life[0]
        if target["type"] == UNIT_WIZARD or target["type"] == UNIT_BUILDING:
            return target
        if target["unit"].life <= damage:
            return target
        for enemy in enemies_by_life:
            if enemy["type"] == UNIT_WIZARD:
                return enemy
        for enemy in enemies_by_life:
            if enemy["type"] == UNIT_BUILDING:
                return enemy
        return target


    def battle_engine(self, me: Wizard, world: World, game: Game, move: Move, enemies_in_range):
        enemies_in_cast_range = [enemy for enemy in enemies_in_range if enemy["dist"] + me.radius <= me.cast_range]
        enemies_in_staff_range = [enemy for enemy in enemies_in_range if enemy["dist"] <= game.staff_range+enemy["unit"].radius+me.radius]

        if len(enemies_in_staff_range) > 0:
            target = self.select_unit_for_attack(enemies_in_staff_range, game.staff_damage)
            angle = me.get_angle_to_unit(target["unit"])
            move.turn = angle
            if me.remaining_action_cooldown_ticks == 0 and \
                me.remaining_cooldown_ticks_by_action[ActionType.STAFF]==0:
                move.action = ActionType.STAFF

        elif len(enemies_in_cast_range) > 0 and move.action != ActionType.STAFF:
            target = self.select_unit_for_attack(enemies_in_cast_range, game.magic_missile_direct_damage)
            angle = me.get_angle_to_unit(target["unit"])
            move.turn = angle
            if me.remaining_action_cooldown_ticks == 0 and \
                me.remaining_cooldown_ticks_by_action[ActionType.MAGIC_MISSILE]==0:

                move.min_cast_distance = target["dist"] - target["unit"].radius + game.magic_missile_radius
                move.max_cast_distance = target["dist"] + target["unit"].radius + game.magic_missile_radius
                move.action = ActionType.MAGIC_MISSILE

        threats, direct_threats, allies = self.scan_aroud(me, world, game)

        if move.action!=ActionType.STAFF and move.action!=ActionType.MAGIC_MISSILE:
            if len(direct_threats) > 1 or me.life < game.wizard_base_life/4:
                obstacle, type = self.find_nearest_obstacle_in_behind(me, world)
                if obstacle is None:
                    move.speed = -game.wizard_forward_speed
                else:
                    move.strafe_speed = -sign(me.get_angle_to_unit(obstacle))*game.wizard_strafe_speed
            else:
                target = self.select_unit_for_attack(enemies_in_staff_range, game.staff_damage)
                if target is not None:
                    move.turn = me.get_angle_to_unit(target["unit"])
                    move.speed = game.wizard_forward_speed
                else:
                    target = self.select_unit_for_attack(enemies_in_range, game.magic_missile_direct_damage)
                    if target is not None:
                        move.turn = me.get_angle_to_unit(target["unit"])
                        if me.get_distance_to_unit(target["unit"]) > me.cast_range*0.75 and \
                                ((len(allies) >= len(threats) - 1 and me.life > game.wizard_base_life/3) or \
                                 target["unit"].life < game.magic_missile_direct_damage*4):
                            move.speed = game.wizard_forward_speed
                    else:
                        move.speed = game.wizard_forward_speed
                obstacle, type = self.find_nearest_obstacle_in_front(me, world)
                if obstacle is not None:
                    move.strafe_speed = -sign(me.get_angle_to_unit(obstacle))*game.wizard_strafe_speed
                    move.speed = 0


    def respawned(self, me):
        return self.last_coors is None or me.get_distance_to(self.last_coors[0], self.last_coors[1]) > 100

    def select_new_goal(self, me: Wizard, world: World):
        if self.wait_for_bonus == True and world.tick_index % 2500 > 2000:
            return
        else:
            self.wait_for_bonus = False
        if self.mode==GO_TO_LANE:
            self.current_goal = self.enemy_base_coors
            self.mode = GO_TO_ENEMY_BASE



    def find_nearest_waypoint(self, me):
        waypoints = list(GRAPH.keys())
        waypoints.sort(key = lambda waypoint: me.get_distance_to(waypoint[0], waypoint[1]))
        return waypoints[0]


    def find_nearest_bonus(self, me: Wizard, world: World):
        for bonus in world.bonuses:
            if me.get_distance_to_unit(bonus) < 600:
                return bonus
        return None


    def waypoint_engine(self, me:Wizard, world: World, game: Game, move: Move):
        nearest_waypoint = self.find_nearest_waypoint(me)
        if self.return_to_track:
            if me.get_distance_to(nearest_waypoint[0], nearest_waypoint[1]) < 70:
                self.return_to_track = False

        nearest_bonus = self.find_nearest_bonus(me, world)
        if nearest_bonus is not None:
            self.wait_for_bonus = False
            goal = (nearest_bonus.x, nearest_bonus.y)
        elif self.return_to_track:
            goal = nearest_waypoint
        else:
            if len(self.path_macro) == 0:
                self.path_macro = pathfinder_macro(nearest_waypoint, self.current_goal)
            goal = self.path_macro[-1]


        if world.tick_index % 2 == 0 or len(self.path_micro) == 0:
            obstacles = self.build_obstacles_list(me, world)
            self.path_micro = pathfinder_micro(me, obstacles, (me.x, me.y), goal)
            self.path_micro.pop()
        next_point = self.path_micro.pop()
        forward_speed, strafe_speed = self.calc_speeds(me, next_point[0], next_point[1])
        move.speed = forward_speed
        move.strafe_speed = strafe_speed
        move.turn = me.get_angle_to(goal[0], goal[1])
        if len(self.path_micro) == 0:
            self.path_macro = pathfinder_macro(nearest_waypoint, self.current_goal)


    def calc_speeds(self, me: Wizard, x, y):
        dist = me.get_distance_to(x, y)
        angle = me.get_angle_to(x, y)
        forward_speed = math.cos(angle)*dist
        strafe_speed = math.sin(angle)*dist

        if strafe_speed == 0:
            if forward_speed > 0:
                return 4,0
            else:
                return -3,0

        if forward_speed > 0:
            if abs(forward_speed / strafe_speed) > 4.0/3.0:
                total_forward_speed = 4
                total_strafe_speed = strafe_speed * total_forward_speed / forward_speed
            else:
                total_strafe_speed = 3*sign(strafe_speed)
                total_forward_speed = forward_speed * total_strafe_speed / strafe_speed
        else:
            if abs(forward_speed / strafe_speed) > 3.0/3.0:
                total_forward_speed = -3
                total_strafe_speed = strafe_speed * total_forward_speed / forward_speed
            else:
                total_strafe_speed = 3*sign(strafe_speed)
                total_forward_speed = forward_speed * total_strafe_speed / strafe_speed
        return total_forward_speed, total_strafe_speed



    def move(self, me: Wizard, world: World, game: Game, move: Move):
        if self.respawned(me):
            self.path_micro = []
            self.path_micro = []
            self.fightning = False
            self.return_to_track = False
            if me.x < world.width/2:
                self.my_base_coors = (400, 3600)
                self.enemy_base_coors = (3600, 400)
            else:
                self.my_base_coors = (3600, 400)
                self.enemy_base_coors = (400, 3600)

            rr = random.randint(0,2)
            rr = 2
            self.current_goal = WAYPOINTS[LANE_NAMES[rr]]
            self.mode = GO_TO_LANE

        for message in me.messages:
            if message.lane == LaneType.TOP:
                self.current_goal = WAYPOINTS["top_lane"]
            elif message.lane == LaneType.MIDDLE:
                self.current_goal = WAYPOINTS["center_lane"]
            elif message.lane == LaneType.BOTTOM:
                self.current_goal = WAYPOINTS["bottom_lane"]


        self.last_coors = (me.x, me.y)

        '''if world.tick_index % 2500 > 2300 and world.tick_index % 2500 < 2500:
            locations_to_wait = [(1000,1000), (1400,1400),(2600,2600),(3000,3000)]
            locations_to_wait.sort(key = lambda loc: me.get_distance_to(loc[0], loc[1]))
            closest = locations_to_wait[0]
            if me.get_distance_to(closest[0], closest[1]) < 1000:
                self.current_goal = closest
                self.wait_for_bonus = True
        if world.tick_index % 2500 > 300 and self.wait_for_bonus:
            self.wait_for_bonus = False
            self.select_new_goal(me, world)'''

        enemies_in_range = self.find_enemies_nearby(me, world)
        if len(enemies_in_range) == 0:
            if self.fightning:
                self.fightning = False
                self.return_to_track = True

            self.waypoint_engine(me, world, game, move)
            if len(self.path_macro) == 0 or me.get_distance_to(self.current_goal[0], self.current_goal[1]) < 70:
                self.select_new_goal(me, world)
        else:
            self.fightning = True
            self.battle_engine(me, world, game, move, enemies_in_range)
