import random, math

from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World
from model.LaneType import LaneType
from model.Faction import Faction
from model.BuildingType import BuildingType
from model.MinionType import MinionType
from model.Minion import Minion
from model.Bonus import Bonus
from model.BonusType import BonusType
from model.Unit import Unit
from model.LivingUnit import LivingUnit


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
        GRAPH[base1N[1]] = [base1N[0], base1N[2], base1E[1], base1W[1]]
        GRAPH[base1N[2]] = [base1N[1], base1NE]
        GRAPH[base1E[0]] = [base1NE, base1E[1]]
        GRAPH[base1E[1]] = [base1E[0], base1E[2], base1N[1], base1S[1]]
        GRAPH[base1E[2]] = [base1SE, base1E[1]]
        GRAPH[base1S[0]] = [base1SE, base1S[1]]
        GRAPH[base1S[1]] = [base1S[0], base1S[2], base1E[1], base1W[1]]
        GRAPH[base1S[2]] = [base1SW, base1S[1]]
        GRAPH[base1W[0]] = [base1SW, base1W[1]]
        GRAPH[base1W[1]] = [base1W[0], base1W[2], base1S[1], base1N[1]]
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
        GRAPH[base2N[1]] = [base2N[0], base2N[2], base2W[1], base2E[1]]
        GRAPH[base2N[2]] = [base2N[1], base2NE]
        GRAPH[base2E[0]] = [base2NE, base2E[1]]
        GRAPH[base2E[1]] = [base2E[0], base2E[2], base2N[1], base2S[1]]
        GRAPH[base2E[2]] = [base2SE, base2E[1]]
        GRAPH[base2S[0]] = [base2SE, base2S[1]]
        GRAPH[base2S[1]] = [base2S[0], base2S[2], base2E[1], base2W[1]]
        GRAPH[base2S[2]] = [base2SW, base2S[1]]
        GRAPH[base2W[0]] = [base2SW, base2W[1]]
        GRAPH[base2W[1]] = [base2W[0], base2W[2], base2N[1], base2S[1]]
        GRAPH[base2W[2]] = [base2NW, base2W[1]]


        #3200-400
        west_lane = []
        for y in range(3200, 300,-100):
            west_lane.append((200, y))

        north_lane = []
        #400-3200
        for x in range(400, 3300, 100):
            north_lane.append((x, 200))

        #800-3600
        east_lane = []
        for y in range(800, 3700, 100):
            east_lane.append((3800, y))

        #3600-800
        south_lane = []
        for x in range(3600, 700, -100):
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
        for shift in range(700,2000,100):
            NE_to_center_lane.append((4000-shift, shift))
            SW_to_center_lane.append((shift, 4000-shift))
        for shift in range(400,2000,100):
            NW_to_center_lane.append((shift, shift))
            SE_to_center_lane.append((4000-shift, 4000-shift))
        del SW_to_center_lane[0]
        del NE_to_center_lane[0]

        GRAPH[west_lane[-1]].append(NW_to_center_lane[0])
        GRAPH[north_lane[0]].append(NW_to_center_lane[0])
        GRAPH[west_lane[-2]].append(NW_to_center_lane[0])
        GRAPH[north_lane[1]].append(NW_to_center_lane[0])

        GRAPH[base2SW].append(NE_to_center_lane[0])

        GRAPH[east_lane[-1]].append(SE_to_center_lane[0])
        GRAPH[south_lane[0]].append(SE_to_center_lane[0])
        GRAPH[east_lane[-2]].append(SE_to_center_lane[0])
        GRAPH[south_lane[1]].append(SE_to_center_lane[0])

        GRAPH[base1NE].append(SW_to_center_lane[0])

        GRAPH[NW_to_center_lane[0]] = [west_lane[-1], north_lane[0], NW_to_center_lane[1], west_lane[-2], north_lane[1]]
        GRAPH[NE_to_center_lane[0]] = [base2SW, NE_to_center_lane[1]]
        GRAPH[SE_to_center_lane[0]] = [east_lane[-1], south_lane[0], SE_to_center_lane[1], east_lane[-2], south_lane[1]]
        GRAPH[SW_to_center_lane[0]] = [base1NE, SW_to_center_lane[1]]
        
        for i in range(1, len(NW_to_center_lane)-1):
            GRAPH[NW_to_center_lane[i]] = [NW_to_center_lane[i-1], NW_to_center_lane[i+1]]
        GRAPH[NW_to_center_lane[-1]] = [NW_to_center_lane[-2], center, NE_to_center_lane[-1], SW_to_center_lane[-1]]
        
        for i in range(1, len(NE_to_center_lane)-1):
            GRAPH[NE_to_center_lane[i]] = [NE_to_center_lane[i-1], NE_to_center_lane[i+1]]
        GRAPH[NE_to_center_lane[-1]] = [NE_to_center_lane[-2], center, NW_to_center_lane[-1], SE_to_center_lane[-1]]
        
        for i in range(1, len(SE_to_center_lane)-1):
            GRAPH[SE_to_center_lane[i]] = [SE_to_center_lane[i-1], SE_to_center_lane[i+1]]
        GRAPH[SE_to_center_lane[-1]] = [SE_to_center_lane[-2], center, NE_to_center_lane[-1], SW_to_center_lane[-1]]
        
        for i in range(1, len(SW_to_center_lane)-1):
            GRAPH[SW_to_center_lane[i]] = [SW_to_center_lane[i-1], SW_to_center_lane[i+1]]
        GRAPH[SW_to_center_lane[-1]] = [SW_to_center_lane[-2], center, NW_to_center_lane[-1], SE_to_center_lane[-1]]
        
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

MICRO_STEP = 5
def pathfinder_micro(me: Wizard, obstacles, start, goal):
    if math.hypot(start[0]-goal[0], start[1]-goal[1]) <= MICRO_STEP:
        return [start, goal]

    start = (int(start[0]), int(start[1]))
    goal = (int(goal[0]), int(goal[1]))
    open_nodes = [{'node': start, 'dist':0, 'f': math.hypot(start[0]-goal[0], start[1]-goal[1])}]
    closed_nodes = set()
    parents = {}


    while len(open_nodes) > 0:
        st = open_nodes.pop(0)
        node = st['node']
        dist = st['dist']
        closed_nodes.add(node)
        candidates = [(node[0] - MICRO_STEP, node[1] - MICRO_STEP),
                      (node[0] - MICRO_STEP, node[1] + MICRO_STEP),
                      (node[0] + MICRO_STEP, node[1] + MICRO_STEP),
                      (node[0] + MICRO_STEP, node[1] - MICRO_STEP)]
        if abs(node[1]-goal[1]) < 5 and abs(node[0]-goal[0]) < 5:
            candidates.append((goal[0], goal[1]))
        if abs(node[1]-goal[1]) < 5:
            candidates.append((node[0] - MICRO_STEP, goal[1]))
            candidates.append((node[0] + MICRO_STEP, goal[1]))
        if abs(node[0]-goal[0]) < 5:
            candidates.append((goal[0], node[1] - MICRO_STEP))
            candidates.append((goal[0], node[1] + MICRO_STEP))

        if dist < 5:
            for obstacle in obstacles:
                if math.hypot(node[0] - obstacle['x'], node[1] - obstacle['y']) > obstacle['radius'] + me.radius + 5:
                    continue
                updated_candidates = []
                for candidate in candidates:
                    if math.hypot(candidate[0] - obstacle['x'], candidate[1] - obstacle['y']) > obstacle['radius'] + me.radius:
                        updated_candidates.append(candidate)
                candidates = updated_candidates

        for next_node in candidates:
            if math.hypot(next_node[0]-goal[0], next_node[1]-goal[1]) == 0:
                path = [next_node, node]
                back_node = node
                while back_node in parents:
                    path.append(parents[back_node])
                    back_node = parents[back_node]
                return path
            if next_node not in closed_nodes:
                new_dist = dist + 1
                new_f = new_dist+math.hypot(next_node[0]-goal[0], next_node[1]-goal[1])
                index = 0
                while index != len(open_nodes) and open_nodes[index]['f'] + open_nodes[index]['dist'] < new_f + new_dist:
                    index += 1
                if index < len(open_nodes):
                    open_nodes.insert(index, {'node': next_node, 'dist': new_dist, 'f': new_f})
                else:
                    open_nodes.append({'node': next_node, 'dist': new_dist, 'f': new_f})
                parents[next_node] = node
    return [start, goal]


def gradient_func(me: Wizard, world: World, threats, game: Game, target):
    def grad(x,y):
        grad_x = 0
        grad_y = 0

        time_to_shoot_missile = max(me.remaining_action_cooldown_ticks, me.remaining_cooldown_ticks_by_action[ActionType.MAGIC_MISSILE])

        res_x = x
        res_y = y
        dx_retreat = 0
        dy_retreat = 0
        total_threats = 0
        target_threat_distance = 0
        for threat in threats:
            if target is not None and threat["unit"].id == target["unit"].id:
                target_threat_distance=threat["threat_radius"]
            distance_to_unit = math.hypot(x-threat["unit"].x, y-threat["unit"].y)
            threat_distance_diff = distance_to_unit - threat["threat_radius"]
            if me.life < 30:
                threat_distance_diff -= 50
            #Стоим слишком близко и по нам много кто целится - надо отойти за огневой рубеж
            if threat_distance_diff < 0:
                total_threats += 1
                dx_retreat += (x - threat["unit"].x)*abs(threat_distance_diff)/threat["threat_radius"]
                dy_retreat += (y - threat["unit"].y)*abs(threat_distance_diff)/threat["threat_radius"]
            if threat["hp"] <= 0.3:
                #встать поближе к умирающему юниту, чтобы получить очки
                pass

        projectile_at_me = None
        for projectile in world.projectiles:
            if abs(projectile.get_angle_to(x,y)) < math.pi/12 and projectile.get_distance_to(x,y) < 500:
                projectile_at_me = projectile
                break

        bonus = find_nearest_bonus(me, world)
        if not any_enemies_between_me_and_bonus(me, world, bonus):
            return (bonus.x, bonus.y)

        if total_threats > 1:
            res_x = x + dx_retreat
            res_y = y + dy_retreat
        elif target is not None:
            if target["type"] == UNIT_WIZARD:
                best_distance_to_target = me.cast_range - 5  + time_to_shoot_missile*3
            elif target["type"] == UNIT_BUILDING and target_threat_distance < 100:
                best_distance_to_target = 0
            else:
                best_distance_to_target =  me.cast_range - 100
            distance_to_threat = math.hypot(target["unit"].x - x, target["unit"].y - y)
            res_x = target["unit"].x + (x - target["unit"].x)*best_distance_to_target/distance_to_threat
            res_y = target["unit"].y + (y - target["unit"].y)*best_distance_to_target/distance_to_threat


        if res_x < 0:
            res_y += abs(res_x)*sign(res_y-y)
            res_x = x
        elif res_x > 4000:
            res_y += abs(4000-res_x)*sign(res_y-y)
            res_x = x
        elif res_y < 0:
            res_x += abs(res_y)*sign(res_x-x)
            res_y = y
        elif res_y > 4000:
            res_x += abs(4000-res_y)*sign(res_x-x)
            res_y = y
        return (res_x, res_y)
    return grad


def find_nearest_bonus(me: Wizard, world: World):
    bonuses = []
    for bonus in world.bonuses:
        bonuses.append({"bonus": bonus, "dist": me.get_distance_to_unit(bonus)})
    if TOP_BONUS_ACTIVE:
            bonuses.append({"bonus": Bonus(-1, 1150, 1150, 0,0,0,Faction.OTHER, 10, -1), "dist": me.get_distance_to(1150,1150)})
            bonuses.append({"bonus": Bonus(-1, 1250, 1250, 0,0,0,Faction.OTHER, 10, -1), "dist": me.get_distance_to(1250,1250)})
    if BOTTOM_BONUS_ACTIVE:
            bonuses.append({"bonus": Bonus(-1, 2750, 2750, 0,0,0,Faction.OTHER, 10, -1), "dist": me.get_distance_to(2750,2750)})
            bonuses.append({"bonus": Bonus(-1, 2850, 2850, 0,0,0,Faction.OTHER, 10, -1), "dist": me.get_distance_to(2850,2850)})
    bonuses.sort(key=lambda bonus: bonus["dist"])
    if len(bonuses) > 0 and me.get_distance_to(bonuses[0]["bonus"].x, bonuses[0]["bonus"].y) < 1200 and me.get_distance_to(bonuses[0]["bonus"].x, bonuses[0]["bonus"].y) < me.get_distance_to(ENEMY_BASE_COORS[0], ENEMY_BASE_COORS[1]):
        return bonuses[0]["bonus"]
    else:
        return None

def any_enemies_between_me_and_bonus(me: Wizard, world: World, bonus: Bonus):
        if bonus is None:
            return True
        dist = me.get_distance_to_unit(bonus)
        for minion in world.minions:
            if minion.faction != me.faction and \
                            minion.faction!=Faction.NEUTRAL and \
                            minion.get_distance_to_unit(me) < me.cast_range and \
                            minion.get_distance_to_unit(me) < dist and minion.get_distance_to_unit(bonus) < dist:
                return True
        for wizard in world.wizards:
            if wizard.faction != me.faction and \
                            wizard.faction!=Faction.NEUTRAL and \
                            wizard.get_distance_to_unit(me) < me.cast_range and \
                            wizard.get_distance_to_unit(me) < dist and wizard.get_distance_to_unit(bonus) < dist:
                return True
        return False

def find_minimum(x,y,grad_f):
    (delta_x, delta_y) = grad_f(x,y)
    return delta_x, delta_y


def is_point_visible(x, y, world: World, me: Wizard):
    for minion in world.minions:
        if minion.faction == me.faction and minion.get_distance_to(x,y) <= minion.vision_range:
            return True
    for wizard in world.wizards:
        if wizard.faction == me.faction and wizard.get_distance_to(x,y) <= wizard.vision_range:
            return True
    for building in world.buildings:
        if building.faction == me.faction and building.get_distance_to(x,y) <= building.vision_range:
            return True
    return False

#find_path((200, 3400), (3400, 600))
LANE_NAMES = ["top_lane", "center_lane", "bottom_lane"]
WAYPOINTS = {"top_lane": (400,400),
             "center_lane": (2000,2000),
             "bottom_lane": (3600,3600),
             "base1": (200,3800),
             "base2": (3800,200),
             "bonus1": (1200,1200),
             "bonus2": (2800, 2800)}

ENEMY_MINION_SPAWNS = [
    [Minion(-1, 630, 3123,0,0,0,0,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 185, 2951,0,0,0,0,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 243, 2958,0,0,0,0,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 1059, 3873,0,0,0,0,25,100,100,[],MinionType.FETISH_BLOWDART,400,6,30,0),
     Minion(-1, 998, 3905,0,0,0,0,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 847, 3050,0,0,0,0,25,100,100,[],MinionType.FETISH_BLOWDART,400,6,30,0),
     Minion(-1, 201, 3011,0,0,0,0,25,100,100,[],MinionType.FETISH_BLOWDART,400,6,30,0),
     Minion(-1, 105, 3035,0,0,0,0,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 941, 3711,0,0,0,0,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 665, 3082,0,0,0,0,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 803, 3316,0,0,0,0,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 1035, 3947,0,0,0,0,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0)],

    [Minion(-1, 3259, 716,0,0,0,1,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 3356, 785,0,0,0,1,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 2952, 119,0,0,0,1,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 2948, 174,0,0,0,1,25,100,100,[],MinionType.FETISH_BLOWDART,400,6,30,0),
     Minion(-1, 3082, 933,0,0,0,1,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 3176, 724,0,0,0,1,25,100,100,[],MinionType.FETISH_BLOWDART,400,6,30,0),
     Minion(-1, 3833, 903,0,0,0,1,25,100,100,[],MinionType.FETISH_BLOWDART,400,6,30,0),
     Minion(-1, 3768, 812,0,0,0,1,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 2862, 368,0,0,0,1,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 2856, 91,0,0,0,1,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 3966, 837,0,0,0,1,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0),
     Minion(-1, 3636, 1101,0,0,0,1,25,100,100,[],MinionType.ORC_WOODCUTTER,400,12,60,0)]]



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
ENEMY_BASE_COORS = (0,0)
MY_BASE_COORS = (0,0)
TOP_BONUS_ACTIVE = False
BOTTOM_BONUS_ACTIVE = False

def sign(x):
    if x==0:
        return 0
    else:
        return abs(x)/x

class MyStrategy:

    def __init__(self):
        self.mode = START_MODE
        self.last_coors = None
        self.current_goals = []
        self.fightning = False
        self.on_track = False
        self.path_macro = []
        self.wizards_per_lane = {}


    def find_enemies_nearby(self, me:Wizard, world:World):
        result = []
        for wizard in world.wizards:
            if wizard.faction != me.faction and wizard.get_distance_to_unit(me) < me.cast_range*1.3:
                result.append({"dist": wizard.get_distance_to_unit(me), "unit": wizard, "type": UNIT_WIZARD, "real": True})
        for minion in world.minions:
            if minion.faction != me.faction and minion.faction != Faction.NEUTRAL and minion.get_distance_to_unit(me) < me.cast_range*1.3:
                result.append({"dist": minion.get_distance_to_unit(me), "unit":minion, "type":UNIT_MINION, "real": True})
        for building in world.buildings:
            if building.faction != me.faction and building.get_distance_to_unit(me) < me.cast_range*1.3:
                result.append({"dist": building.get_distance_to_unit(me), "unit": building, "type":UNIT_BUILDING, "real": True})
        if world.tick_index % 750 > 700:
            for minion in ENEMY_MINION_SPAWNS[1-me.faction]:
                if minion.get_distance_to_unit(me) < me.cast_range*1.3:
                    result.append({"dist": minion.get_distance_to_unit(me), "unit":minion, "type":UNIT_MINION, "real": False})
        result.sort(key=lambda data: data["dist"])
        return result

    def find_nearest_ally_to_enemy(self, me, enemy, enemy_range, world: World, game: Game):
        dist = 9999
        unit = None
        type = -1
        max_life = 9999

        for wizard in world.wizards:
            if wizard.x == me.x and wizard.y == me.y:
                continue
            if wizard.faction != enemy.faction and wizard.get_distance_to_unit(enemy) < dist and wizard.get_distance_to_unit(enemy) <= enemy_range:
                dist = wizard.get_distance_to_unit(enemy)
                unit = wizard
                type = UNIT_WIZARD
                max_life = game.wizard_base_life
        for minion in world.minions:
            if minion.faction != enemy.faction and minion.faction != Faction.NEUTRAL and minion.get_distance_to_unit(enemy) < dist and minion.get_distance_to_unit(enemy) <= enemy_range:
                dist = minion.get_distance_to_unit(enemy)
                unit = minion
                type = UNIT_MINION
                max_life = game.minion_life
        for building in world.buildings:
            if building.faction != enemy.faction and building.get_distance_to_unit(enemy) < dist and building.get_distance_to_unit(enemy) <= enemy_range:
                dist = building.get_distance_to_unit(enemy)
                unit = building
                type = UNIT_BUILDING
                if building.type == BuildingType.FACTION_BASE:
                    max_life = game.faction_base_life
                else:
                    max_life = game.guardian_tower_life
        if unit is None:
            return None
        return {"unit": unit, "dist": dist, "type":type, "max_life": max_life}

    def scan_around(self, me: Wizard, world: World, game: Game):
        threats = []

        for wizard in world.wizards:
            if wizard.get_distance_to_unit(me) < me.cast_range*2 and wizard.faction != me.faction:
                threat_radius = wizard.cast_range
                threat_target = self.find_nearest_ally_to_enemy(me, wizard, wizard.cast_range, world, game)
                if threat_target is not None and threat_target['dist'] < wizard.cast_range:
                    delta = wizard.cast_range - threat_target['dist']
                    delta *= threat_target['unit'].life / threat_target['max_life']
                    threat_radius = delta + threat_target['dist']
                threats.append({"unit": wizard, "threat_radius": threat_radius, "type": UNIT_WIZARD, "hp": wizard.life/game.wizard_base_life, "real": True})
        for minion in world.minions:
            if minion.get_distance_to_unit(me) < 2*me.cast_range and minion.faction != me.faction and minion.faction != Faction.NEUTRAL:
                threat_radius = game.fetish_blowdart_attack_range
                threat_target = self.find_nearest_ally_to_enemy(me, minion, game.fetish_blowdart_attack_range, world, game)
                if threat_target is not None:
                    if minion.type == MinionType.FETISH_BLOWDART and threat_target['dist'] < game.fetish_blowdart_attack_range:
                        delta = game.fetish_blowdart_attack_range - threat_target['dist']
                        #delta *= threat_target['unit'].life / threat_target['max_life']
                        threat_radius = delta + threat_target['dist']
                threats.append({"unit": minion, "threat_radius": threat_radius, "type": UNIT_MINION, "hp": minion.life / game.minion_life, "real": True})
        for building in world.buildings:
            if building.get_distance_to_unit(me) < 2*me.cast_range and building.faction != me.faction and building.faction != Faction.NEUTRAL:
                if building.type == BuildingType.FACTION_BASE:
                    threat_radius = game.faction_base_attack_range
                else:
                    threat_radius = game.guardian_tower_attack_range
                threat_target = self.find_nearest_ally_to_enemy(me, building, threat_radius, world, game)
                if threat_target is not None:
                    if building.type == BuildingType.FACTION_BASE and threat_target['dist'] < game.faction_base_radius:
                        delta = game.faction_base_radius - threat_target['dist']
                        #delta *= threat_target['unit'].life / threat_target['max_life']
                        threat_radius = delta + threat_target['dist']
                    elif building.type == BuildingType.GUARDIAN_TOWER and threat_target['dist'] < game.guardian_tower_attack_range:
                        delta = game.faction_base_radius - threat_target['dist']
                        #delta *= threat_target['unit'].life / threat_target['max_life']
                        threat_radius = delta + threat_target['dist']

                if building.type == BuildingType.FACTION_BASE:
                    hp = building.life / game.faction_base_life
                else:
                    hp = building.life / game.guardian_tower_life

                threats.append({"unit": building, "threat_radius": threat_radius, "type": UNIT_BUILDING, "hp": hp, "real": True})
        if world.tick_index % 750 > 700:
            for minion in ENEMY_MINION_SPAWNS[1-me.faction]:
                if minion.get_distance_to_unit(me) < 2*me.cast_range:
                    threat_radius = game.fetish_blowdart_attack_range
                    threat_target = self.find_nearest_ally_to_enemy(me, minion, game.fetish_blowdart_attack_range, world, game)
                    if threat_target is not None:
                        if minion.type == MinionType.FETISH_BLOWDART and threat_target['dist'] < game.fetish_blowdart_attack_range:
                            delta = game.fetish_blowdart_attack_range - threat_target['dist']
                            delta *= threat_target['unit'].life / threat_target['max_life']
                            threat_radius = delta + threat_target['dist']
                    threats.append({"unit": minion, "threat_radius": threat_radius, "type": UNIT_MINION, "hp": minion.life / game.minion_life, "real": False})
        return threats



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



    def select_unit_for_attack(self, enemies, damage):
        real_enemies = [enemy for enemy in enemies if enemy['real']]
        if len(real_enemies) == 0:
            return None
        enemies_by_life = sorted(real_enemies, key=lambda enemy: enemy["unit"].life)
        for enemy in enemies_by_life:
            if enemy["type"] == UNIT_WIZARD:
                return enemy
        for enemy in enemies_by_life:
            if enemy["type"] == UNIT_BUILDING:
                return enemy
        return enemies_by_life[0]



    def battle_moving(self, me: Wizard, world: World, move: Move, goal):
        obstacles = self.build_obstacles_list(me, world)
        path_micro = pathfinder_micro(me, obstacles, (me.x, me.y), goal)
        if path_micro is not None and len(path_micro) > 1:
            path_micro.pop()
            next_point = path_micro.pop()
            forward_speed, strafe_speed = self.calc_speeds(me, next_point[0], next_point[1])
            move.speed = forward_speed
            move.strafe_speed = strafe_speed

    def battle_engine(self, me: Wizard, world: World, game: Game, move: Move, enemies_in_range):
        enemies_in_cast_range = [enemy for enemy in enemies_in_range if enemy["dist"] <= me.cast_range]
        enemies_in_half_cast_range = [enemy for enemy in enemies_in_range if enemy["dist"] <= me.cast_range/2]
        enemies_in_staff_range = [enemy for enemy in enemies_in_range if enemy["dist"] <= game.staff_range + enemy["unit"].radius]

        target = self.select_unit_for_attack(enemies_in_staff_range, game.staff_damage)
        if target is not None:
            angle = me.get_angle_to_unit(target["unit"])
            move.turn = me.get_angle_to_unit(target["unit"])
            if me.remaining_action_cooldown_ticks == 0 and \
                me.remaining_cooldown_ticks_by_action[ActionType.STAFF]==0 and \
                abs(angle) < game.staff_sector / 2.0:
                move.action = ActionType.STAFF
        if move.action != ActionType.STAFF:
            test_target = self.select_unit_for_attack(enemies_in_cast_range, game.magic_missile_direct_damage)
            if test_target is not None:
                angle = me.get_angle_to_unit(test_target["unit"])
                move.turn = me.get_angle_to(test_target["unit"].x, test_target["unit"].y)
                if me.remaining_action_cooldown_ticks == 0 and \
                    me.remaining_cooldown_ticks_by_action[ActionType.MAGIC_MISSILE]==0 and \
                    abs(angle) < game.staff_sector / 2.0:
                    target = test_target
                    move.min_cast_distance = target["dist"] - target["unit"].radius + game.magic_missile_radius
                    move.max_cast_distance = target["dist"] + target["unit"].radius + game.magic_missile_radius
                    move.action = ActionType.MAGIC_MISSILE
        if target is None:
            target_in_half_cast_range = self.select_unit_for_attack(enemies_in_half_cast_range, game.magic_missile_direct_damage)
            target_in_cast_range = self.select_unit_for_attack(enemies_in_cast_range, game.magic_missile_direct_damage)
            target_in_view = self.select_unit_for_attack(enemies_in_range, game.magic_missile_direct_damage)
            if target_in_half_cast_range is not None:
                target = target_in_half_cast_range
            if target_in_cast_range is not None:
                target = target_in_cast_range
            if target is None or target_in_view["type"] == UNIT_WIZARD and me.life > 40:
                target = target_in_view
            if target is not None:
                move.turn = me.get_angle_to_unit(target["unit"])

        threats = self.scan_around(me, world, game)
        grad_f = gradient_func(me, world, threats, game, target)
        goal = find_minimum(me.x, me.y, grad_f)
        self.battle_moving(me, world, move, goal)



    def respawned(self, me):
        return self.last_coors is None or me.get_distance_to(self.last_coors[0], self.last_coors[1]) > 100


    def update_goal(self, me: Wizard, world: World):
        global MY_BASE_COORS, ENEMY_BASE_COORS
        if self.respawned(me):
            self.fightning = False
            self.on_track = True
            if me.x < world.width/2:
                MY_BASE_COORS = WAYPOINTS["base1"]
                ENEMY_BASE_COORS = WAYPOINTS["base2"]
            else:
                MY_BASE_COORS = WAYPOINTS["base2"]
                ENEMY_BASE_COORS = WAYPOINTS["base1"]

            lane_waypoint = WAYPOINTS[LANE_NAMES[random.randint(0,2)]]
            for message in me.messages:
                if message.lane == LaneType.TOP:
                    lane_waypoint = WAYPOINTS["top_lane"]
                elif message.lane == LaneType.MIDDLE:
                    lane_waypoint = WAYPOINTS["center_lane"]
                elif message.lane == LaneType.BOTTOM:
                    lane_waypoint = WAYPOINTS["bottom_lane"]
            self.current_goals = [lane_waypoint, ENEMY_BASE_COORS]



        nearest_waypoint = self.find_nearest_waypoint(me)
        nearest_bonus = find_nearest_bonus(me, world)

        if me.get_distance_to(self.current_goals[0][0], self.current_goals[0][1]) <= 200 and self.current_goals[0]!=ENEMY_BASE_COORS:
            self.current_goals.pop(0)
        if me.get_distance_to(nearest_waypoint[0], nearest_waypoint[1]):
            self.on_track = True

        if self.fightning:
            self.fightning = False
            self.on_track = False
            self.current_goals = [nearest_waypoint, ENEMY_BASE_COORS]
        if nearest_bonus is not None:
            self.path_macro = [(me.x, me.y), (nearest_bonus.x, nearest_bonus.y)]
        elif self.on_track:
            self.path_macro = pathfinder_macro(nearest_waypoint, self.current_goals[0])
            self.path_macro.pop()
        else:
            self.path_macro = [(me.x, me.y), nearest_waypoint]





    def find_nearest_waypoint(self, me):
        waypoints = list(GRAPH.keys())
        waypoints.sort(key = lambda waypoint: me.get_distance_to(waypoint[0], waypoint[1]))
        return waypoints[0]





    def waypoint_engine(self, me:Wizard, world: World, game: Game, move: Move):
        goal = self.path_macro[-1]
        obstacles = self.build_obstacles_list(me, world)
        path_micro = pathfinder_micro(me, obstacles, (me.x, me.y), goal)
        if len(path_micro) == 0:
            return False
        path_micro.pop()
        next_point = path_micro.pop()
        forward_speed, strafe_speed = self.calc_speeds(me, next_point[0], next_point[1])
        move.speed = forward_speed
        move.strafe_speed = strafe_speed
        move.turn = me.get_angle_to(goal[0], goal[1])




    def calc_speeds(self, me: Wizard, x, y):
        dist = me.get_distance_to(x, y)
        angle = me.get_angle_to(x, y)
        forward_speed = math.cos(angle)*dist
        strafe_speed = math.sin(angle)*dist
        if forward_speed == 0 and strafe_speed == 0:
            return 0, 0
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


    def update_global_state(self, me: Wizard, world: World):
        global TOP_BONUS_ACTIVE, BOTTOM_BONUS_ACTIVE
        if world.tick_index % 2500 > 2200:
            TOP_BONUS_ACTIVE = True
            BOTTOM_BONUS_ACTIVE = True
        top_bonus_detected = False
        bottom_bonus_detected = False
        for bonus in world.bonuses:
            if bonus.x == 1200:
                top_bonus_detected = True
            if bonus.x == 2800:
                bottom_bonus_detected = True
        if is_point_visible(1200,1200,world,me) and not top_bonus_detected:
            TOP_BONUS_ACTIVE = False
        if is_point_visible(2800,2800,world,me) and not bottom_bonus_detected:
            BOTTOM_BONUS_ACTIVE = False



    def move(self, me: Wizard, world: World, game: Game, move: Move):
        self.update_global_state(me, world)
        enemies_in_range = self.find_enemies_nearby(me, world)
        if len(enemies_in_range) == 0:
            self.update_goal(me, world)
            self.last_coors = (me.x, me.y)
            self.waypoint_engine(me, world, game, move)
        else:
            self.last_coors = (me.x, me.y)
            self.fightning = True
            self.battle_engine(me, world, game, move, enemies_in_range)
