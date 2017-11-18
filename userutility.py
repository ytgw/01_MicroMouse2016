# coding: UTF-8
import common
import numpy as np
import operator

#-----------------------------------------------------------------------------#
# Declation
#-----------------------------------------------------------------------------#
# 壁情報のビット表現
EAST_BIT      = 0b00001
NORTH_BIT     = 0b00010
WEST_BIT      = 0b00100
SOUTH_BIT     = 0b01000
SEARCHED_BIT  = 0b10000
BIT_DIRECTION = [ EAST_BIT, NORTH_BIT, WEST_BIT, SOUTH_BIT ]

#-----------------------------------------------------------------------------#
# Function
#-----------------------------------------------------------------------------#
def rev_array( array ):
    # 配列のxy座標を反転した後に、行を逆転させる
    arrayT = array.transpose()
    revarray = arrayT[::-1]
    return revarray

def calc_next_direcition(nextPosition, presentPosition, presentDirection):
    xDist = nextPosition[0] - presentPosition[0]
    yDist = nextPosition[1] - presentPosition[1]

    nextDirection = presentDirection
    if (xDist != 0) and (yDist != 0):
        print "ERROR in calc_next_direction"
    elif xDist > 0:
        nextDirection = common.EAST
    elif xDist < 0:
        nextDirection = common.WEST
    elif yDist > 0:
        nextDirection = common.NORTH
    elif yDist < 0:
        nextDirection = common.SOUTH

    return nextDirection

def calc_rotate_angle(nextDirection, presentDirection):
    diff = nextDirection - presentDirection

    if diff == 0:
        rotateAngle = 0
    elif (diff == 1) or (diff == -3):
        rotateAngle = 90
    elif (diff == 2) or (diff == -2):
        rotateAngle = 180
    elif (diff == 3) or (diff == -1):
        rotateAngle = -90
    else:
        print "ERROR in calc_rotate_angle"

    return rotateAngle

def calc_distance(nextPosition, presentPosition):
    xDist = nextPosition[0] - presentPosition[0]
    yDist = nextPosition[1] - presentPosition[1]

    if (xDist != 0) and (yDist != 0):
        print "ERROR in calc_distance"

    distance = max([abs(xDist),abs(yDist)])
    return distance

#-----------------------------------------------------------------------------#
# Class
#-----------------------------------------------------------------------------#
# 迷路クラス
class Maze:
    def __init__( self ):
        # self.N = 16                     # 迷路サイズ = N*N
        self.N = 8                     # 迷路サイズ = N*N
        self.MIN_STEP = 0               # ゴール座標の歩数
        self.direction = NORTH_BIT   # 現在の向き
        self.n_dist = [ 0, 0, 0, 0 ]

        # 全区画分の壁情報の宣言と初期化
        self.wallinfo = np.zeros( (self.N, self.N), dtype=np.int)

        self.wallinfo[ tuple(common.INITIAL_POSITION) ] = (EAST_BIT | WEST_BIT | SOUTH_BIT | SEARCHED_BIT)
        # 全区画分の距離情報の宣言と初期化
        self.distinfo = 255 * np.ones( (self.N, self.N), dtype=np.int )
        for pos in common.GOAL_POSITIONS:
            self.distinfo[ tuple(pos) ] = self.MIN_STEP


    #-----------------------------------------------------------------------------#
    # Display Method
    #-----------------------------------------------------------------------------#
    def display_wallinfo( self ):
        # 地図情報をコマンドラインに表示する
        tempinfo = self.wallinfo
        tempinfo = rev_array( tempinfo )
        print "wallinfo = "
        print tempinfo  & 0b11101111


    def display_distinfo( self ):
        # 距離情報をコマンドラインに表示する
        tempinfo = self.distinfo
        tempinfo = rev_array( tempinfo )
        print "distinfo = "
        print tempinfo


    #-----------------------------------------------------------------------------#
    # Get Method
    #-----------------------------------------------------------------------------#
    def get_next_info( self, position, direction, mode):
        #------ 次座標と次方向の算出 -----#
        (nextPosition, nextDirection) = self.get_next_pos_direction(position, direction, mode)
        #----- 回転角度の算出 -----#
        nextAngle = calc_rotate_angle(nextDirection,direction)
        #----- 直進距離の算出 -----#
        nextDist = calc_distance(nextPosition,position)

        return (nextPosition, nextDirection, nextAngle, nextDist)


    def get_next_pos_direction( self, position, direction, mode):
        nextPosition  = position
        nextDirection = direction

        #----- 再帰処理 -----#
        while True:
            virtualPresentPosition  = nextPosition
            virtualPresentDirection = nextDirection

            #------ 次座標の算出 -----#
            if virtualPresentPosition in common.GOAL_POSITIONS:
                # ゴールに到着している場合
                nextPosition  = virtualPresentPosition
            else:
                # ゴールに未到着の場合
                nghbrs  = self.get_neighbor_pos(virtualPresentPosition)[0]
                nowwall = self.wallinfo[tuple(virtualPresentPosition)]

                # 距離情報の更新
                self.update_dist_info(mode)

                # 隣接座標のゴールまでの距離
                nghbrsDist = [255,255,255,255]
                for i in range(len(nghbrsDist)):
                    nghbrsDist[i] = self.distinfo[ tuple(nghbrs[i]) ]
                    if ( nowwall & BIT_DIRECTION[i] ) != 0:
                        # BIT_DIRECTION = [ EAST_BIT, NORTH_BIT, WEST_BIT, SOUTH_BIT ]
                        # 壁がある場合はその方向に進まないようにする
                        # ( min関数でindexが選ばれないようにするために255を代入 )
                        nghbrsDist[i] = 255

                # 歩数が最小の隣接座標を候補にする
                min_index = [i  for i,x in enumerate(nghbrsDist)  if x==min(nghbrsDist)]
                candidate = [nghbrs[x]  for x in min_index]

                # 未探索の区画があれば優先して候補にする
                notSearchedCandidate = [x  for x in candidate  if (self.wallinfo[tuple(x)] & SEARCHED_BIT) == 0]
                if len(notSearchedCandidate) != 0:
                    candidate = notSearchedCandidate

                # 方向転換が少ない隣接座標を優先する
                minimumAngle = 180
                for x in candidate:
                    candidateDirection = calc_next_direcition(x,virtualPresentPosition,virtualPresentDirection)
                    candidateAngle = calc_rotate_angle(candidateDirection,virtualPresentDirection)
                    if abs(candidateAngle) <= minimumAngle:
                        minimumAngle = abs(candidateAngle)
                        finalCandidate = x

                nextPosition = finalCandidate

            #----- 次方向の算出 -----#
            nextDirectionCandidate = calc_next_direcition(nextPosition,virtualPresentPosition,virtualPresentDirection)

            #----- 再帰終了条件 -----#
            if (virtualPresentPosition in common.GOAL_POSITIONS)\
            or ((self.wallinfo[tuple(virtualPresentPosition)] & SEARCHED_BIT) == 0)\
            or ((nextDirection != nextDirectionCandidate) and (position != virtualPresentPosition)):
                # 現在地がゴール or 未探索区画の場合 or 方向変換なし
                nextPosition  = virtualPresentPosition
                nextDirection = virtualPresentDirection
                break
            else:
                nextDirection = nextDirectionCandidate

        return (nextPosition, nextDirection)


    def get_neighbor_pos( self, center ):
        # 引数(center)の上下左右の座標を取得する
        # 引数
        #   center : (x,y)座標。2要素を持つリスト形式かタプル形式で指定。
        # 返り値
        #   neighbors : center の上下左右の座標を表す(x,y)座標が4個含まれるリスト。
        #   chk_flg : center の上下左右座標が壁の向こうを表していたらFalseを返す4要素のリスト。
        chk_flag  = [ True, True, True, True ]
        n_right   = tuple( map(operator.add, list(center), [ 1, 0]) )
        n_top     = tuple( map(operator.add, list(center), [ 0, 1]) )
        n_left    = tuple( map(operator.add, list(center), [-1, 0]) )
        n_bottom  = tuple( map(operator.add, list(center), [ 0,-1]) )
        neighbors = [ n_right , n_top , n_left , n_bottom ]
        for i,chk in enumerate( neighbors ):
            if ( chk[0] >= self.N ) or ( chk[1] >= self.N ) or ( chk[0] <  0 ) or ( chk[1] < 0 ):
                neighbors[ i ] = center
                chk_flag[ i ] = False
        return neighbors, chk_flag


    #-----------------------------------------------------------------------------#
    # Set Method
    #-----------------------------------------------------------------------------#
    def set_wall_info( self, position, direction, wallInfoFromRcg):
        #----- センサからの壁情報を変換 -----#
        convertedWallInfo = 0
        rightWall = wallInfoFromRcg[common.RIGHT]
        frontWall = wallInfoFromRcg[common.FRONT]
        leftWall  = wallInfoFromRcg[common.LEFT]
        if direction == common.EAST:
            convertedWallInfo |= (frontWall * EAST_BIT)
            convertedWallInfo |= (leftWall  * NORTH_BIT)
            convertedWallInfo |= (0         * WEST_BIT)
            convertedWallInfo |= (rightWall * SOUTH_BIT)
        elif direction == common.NORTH:
            convertedWallInfo |= (rightWall * EAST_BIT)
            convertedWallInfo |= (frontWall * NORTH_BIT)
            convertedWallInfo |= (leftWall  * WEST_BIT)
            convertedWallInfo |= (0         * SOUTH_BIT)
        elif direction == common.WEST:
            convertedWallInfo |= (0         * EAST_BIT)
            convertedWallInfo |= (rightWall * NORTH_BIT)
            convertedWallInfo |= (frontWall * WEST_BIT)
            convertedWallInfo |= (leftWall  * SOUTH_BIT)
        elif direction == common.SOUTH:
            convertedWallInfo |= (leftWall  * EAST_BIT)
            convertedWallInfo |= (0         * NORTH_BIT)
            convertedWallInfo |= (rightWall * WEST_BIT)
            convertedWallInfo |= (frontWall * SOUTH_BIT)
        else:
            print "WARNING:undefined direction"

        #----- 変換後の壁情報をセット -----#
        # print "wallForMaze:", convertedWallInfo
        self.set_wallinfo(position, convertedWallInfo)


    def set_wallinfo( self, set_pos, new_wallinfo ):
        # 壁情報を更新
        # 引数
        #   set_pos : 壁情報を更新したい(x,y)座標。2要素を持つリスト形式かタプル形式で指定。
        #   new_wallinfo : 更新する壁情報の値
        # 注目座標の壁情報の更新
        self.wallinfo[ tuple(set_pos) ] |= new_wallinfo
        self.wallinfo[ tuple(set_pos) ] |= SEARCHED_BIT
        # 隣接座標の壁情報の更新
        wallinfo =  self.wallinfo[ tuple(set_pos) ]
        nghbrs, chk = self.get_neighbor_pos( set_pos )
        # 右にマスがあった場合、右のマスに「左に壁」情報をセットする
        if ( (wallinfo & EAST_BIT)  != 0 ) and (chk[0] == True):
            self.wallinfo[ tuple(nghbrs[0]) ] |= WEST_BIT
        # 上にマスがあった場合、上のマスに「下に壁」情報をセットする
        if ( (wallinfo & NORTH_BIT) != 0 ) and (chk[1] == True):
            self.wallinfo[ tuple(nghbrs[1]) ] |= SOUTH_BIT
        # 左にマスがあった場合、左のマスに「右に壁」情報をセットする
        if ( (wallinfo & WEST_BIT)  != 0 ) and (chk[2] == True):
            self.wallinfo[ tuple(nghbrs[2]) ] |= EAST_BIT
        # 下にマスがあった場合、下のマスに「上に壁」情報をセットする
        if ( (wallinfo & SOUTH_BIT) != 0 ) and (chk[3] == True):
            self.wallinfo[ tuple(nghbrs[3]) ] |= NORTH_BIT


    #-----------------------------------------------------------------------------#
    # Other Method
    #-----------------------------------------------------------------------------#
    def update_dist_info( self, mode ):
        # 足立法で各マスの距離情報を取得する
        step = self.MIN_STEP
        flag = True
        # 全区画分の距離情報の初期化
        self.distinfo = 255 * np.ones( (self.N, self.N), dtype=np.int )
        for pos in common.GOAL_POSITIONS:
            self.distinfo[ tuple(pos) ] = self.MIN_STEP

        # ゴール地点からスタート地点までの距離を求めたら処理をやめる
        while flag == True:
            # 歩数マップの更新がある限り処理を続ける
            flag = False
            for x in range( self.N ):
                for y in range( self.N ):
                    cntr =(x,y)
                    if self.distinfo[cntr] == step:
                        nghbrs = self.get_neighbor_pos(cntr)[ 0 ]
                        # 上下左右マスの歩数マップを更新
                        for dr in range( len(BIT_DIRECTION) ):
                            if ( (self.wallinfo[ tuple(cntr) ] & BIT_DIRECTION[dr] ) == 0 )\
                            and ( self.distinfo[ tuple(nghbrs[dr]) ] > self.distinfo[ tuple(cntr) ] ):
                                # 壁がない　かつ　歩数が小さくなる場合
                                if mode == common.SEARCH_MODE:
                                    # 探索モードの場合
                                    self.distinfo[ tuple(nghbrs[dr]) ] = 1 + self.distinfo[ tuple(cntr) ]
                                    flag = True
                                elif (mode == common.FAST_MODE)\
                                and ( ( self.wallinfo[ tuple(nghbrs[dr]) ] & SEARCHED_BIT ) != 0 ):
                                    # 最速モードの場合は探索済み区画のみ更新
                                    self.distinfo[ tuple(nghbrs[dr]) ] = 1 + self.distinfo[ tuple(cntr) ]
                                    flag = True
            step += 1


if __name__ == '__main__':
    testMaze = Maze()
    print "test code is not written."
