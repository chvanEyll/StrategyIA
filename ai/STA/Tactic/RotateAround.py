
# Under MIT licence, see LICENCE.txt

from ai.STA.Tactic.Tactic import Tactic
from ai.STA.Action.MoveToPosition import MoveToPosition
from ai.STA.Action.Idle import Idle
from RULEngine.Util.area import player_close_to_ball_facing_target, angle_to_origin_then_target_is_tolerated, closeToPointFacingTarget
from RULEngine.Util.geometry import rotate_point_around_origin, get_required_kick_force, get_distance, get_angle
from RULEngine.Util.constant import PLAYER_PER_TEAM, ANGLE_TO_HALT
from RULEngine.Util.Pose import Pose
from ai.STA.Tactic.tactic_constants import Flags

__author__ = 'RoboCupULaval'


class RotateAround(Tactic):
    """
    méthodes:
        exec(self) : Exécute une Action selon l'état courant
    attributs:
        info_manager: référence à la façade InfoManager
        player_id : Identifiant du joueur auquel est assigné la tactique
        current_state : L'état courant de la tactique
        next_state : L'état suivant de la tactique
    """

    def __init__(self, game_state, player_id, origin, target):
        Tactic.__init__(self, game_state, player_id, target)
        assert isinstance(player_id, int)
        assert PLAYER_PER_TEAM >= player_id >= 0
        self.status_flag = Flags.INIT
        self.origin = self.game_state.get_ball_position()#origin #hack
        self.current_state = self.check_success
        self.next_state = self.check_success

    def check_success(self):
        self.origin = self.game_state.get_ball_position()  # origin #hack
        self.player_pos = self.game_state.get_player_pose(self.player_id).position
        if angle_to_origin_then_target_is_tolerated(self.player_pos, self.origin, self.target.position, ANGLE_TO_HALT):
            self.status_flag = Flags.SUCCESS
            self.next_state = self.halt
        else:
            self.status_flag = Flags.WIP
            self.next_state = self.rotate_around
        return Idle(self.game_state, self.player_id)

    def rotate_around(self):
        self.origin = self.game_state.get_ball_position()  # origin #hack
        self.player_pos = self.game_state.get_player_pose(self.player_id).position
        # check if counter clockwise
        constant_angle_increment = 1
        if get_angle(self.player_pos, self.target.position) < 0:
            constant_angle_increment *= -1

        # calculate new pose
        new_position = rotate_point_around_origin(self.player_pos, self.origin, constant_angle_increment)
        new_orientation = get_angle(new_position, self.target.position)
        print(new_position)
        print(new_orientation)
        new_pose = Pose(new_position, new_orientation)
        #TODO: goal:print
        #print(self.game_state.get_player_pose(1).position)

        # return command
        self.next_state = self.check_success
        go_to_position = MoveToPosition(self.game_state, self.player_id, new_pose)
        return go_to_position


