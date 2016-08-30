# coding: UTF-8
import os
import time
import middleware as mw
import numpy as np

#-----------------------------------------------------------------------------#
# Declation                                                                  #
#-----------------------------------------------------------------------------#
# スタート地点、ゴール地点、ゴールへの侵入経路の座標 ( x  , y )
start = ( 0  , 0 )
# ゴール座標は事前に分からない?
# goal  = ( (  2 , 12 ) , (  3 , 12 ) ,  (  2 , 11 ) , (  3 , 11 ) )
route = (  3 , 11 )
# 壁情報のビット表現
RIGHT  = 0b00000001
TOP    = 0b00000010
LEFT   = 0b00000100
BOTTOM = 0b00001000
SERCH_COMPLETE = 0b00010000
DIRECTION = [ RIGHT, TOP, LEFT, BOTTOM]
# 配列内の要素番号の意味を分かりやすくするための宣言
POS_X  = 0
POS_Y  = 1

#-----------------------------------------------------------------------------#
# Class                                                                       #
#-----------------------------------------------------------------------------#
# 迷路クラス
class Maze:
    def __init__(self):
        # wallinfo[ y ][ x ]
        #  0bit: 0 = 右に壁なし, 1 = 右に壁あり
        #  1bit: 0 = 上に壁なし, 1 = 上に壁あり
        #  2bit: 0 = 左に壁なし, 1 = 左に壁あり
        #  3bit: 0 = 下に壁なし, 1 = 下に壁あり
        #  4bit: 0 = マスの探索未完了, 1 = マスの探索完了
        self.N = 16
        self.minstep = 1
        self.n_dist = [ 0, 0, 0, 0]
        # 壁情報を数字の0で初期化する
        self.wallinfo = np.array( [ [0] * self.N] * self.N )
        #for pos in goal:
        #    self.wallinfo[ pos[ POS_X ] ][ pos[ POS_Y ] ] = 255
        self.wallinfo[ route[ POS_X ] ][ route[ POS_Y ] ] = 0
        # distinfo[ y ][ x ]
        #  0 ～ 255で距離情報を表す
        # 距離情報を数字の255で初期化する
        self.distinfo = np.array( [ [255] * self.N] * self.N )
        self.distinfo[ start[ POS_X ]  ][ start[ POS_Y ]  ] = 255
        #for pos in goal:
        #    self.distinfo[ pos[ POS_X ] ][ pos[ POS_Y ] ] = 255
        self.distinfo[ route[ POS_X ] ][ route[ POS_Y ] ] = 1
    def get_wallinfo(self):
        return self.wallinfo
    def set_wallinfo(self,set_pos,new_wallinfo):
        # 地図情報を更新
        self.wallinfo[ set_pos[ POS_X ] ][ set_pos[ POS_Y ] ] |= ( 0b00001111 & new_wallinfo )
        wallinfo =  self.wallinfo[ set_pos[ POS_X ] ][ set_pos[ POS_Y ] ]
        nghbrs, chk = self.neighbor_pos(set_pos)
        # 右にマスがあった場合、右のマスに「左に壁」情報をセットする
        if ( ( wallinfo & RIGHT ) == RIGHT ) and (chk[0] == True):
            self.wallinfo[ nghbrs[ 0 ][ POS_X ] ][ nghbrs[ 0 ][ POS_Y ] ] |= LEFT  
        # 上にマスがあった場合、上のマスに「下に壁」情報をセットする
        if ( ( wallinfo & TOP ) == TOP ) and (chk[1] == True):
            self.wallinfo[ nghbrs[ 1 ][ POS_X ] ][ nghbrs[ 1 ][ POS_Y ] ] |= BOTTOM  
        # 左にマスがあった場合、左のマスに「右に壁」情報をセットする
        if ( ( wallinfo & LEFT ) == LEFT ) and (chk[2] == True):
            self.wallinfo[ nghbrs[ 2 ][ POS_X ] ][ nghbrs[ 2 ][ POS_Y ] ] |= RIGHT  
        # 下にマスがあった場合、下のマスに「上に壁」情報をセットする
        if ( ( wallinfo & BOTTOM ) == BOTTOM ) and (chk[3] == True):
            self.wallinfo[ nghbrs[ 3 ][ POS_X ] ][ nghbrs[ 3 ][ POS_Y ] ] |= TOP  
        # 探索完了
        self.wallinfo[ set_pos[ POS_X ] ][ set_pos[ POS_Y ] ] |= ( SERCH_COMPLETE ) 
    def display_wallinfo(self):
        # 地図情報を表示する
        self.wallinfo = rev_array(self.wallinfo, self.N)
        print "wallinfo = "
        print self.wallinfo  & 0b11101111
    def get_distinfo(self):
        # 地図情報を取得する
        return self.distinfo
    def set_distinfo(self,set_pos,new_distinfo):
        # 距離情報を更新する
        self.distinfo[ set_pos[0] ][ set_pos[ POS_Y ] ]  = new_distinfo
    def display_distinfo(self):
        # 距離情報を表示する
        self.distinfo = rev_array(self.distinfo, self.N)
        print "distinfo = "
        print self.distinfo
    def adachi(self):
        # 足立法で各マスの距離情報を取得する
        step = self.minstep
        flag = True
        self.distinfo = np.array( [ [255] * self.N] * self.N )
        self.distinfo[ route[ POS_X ] ][ route[ POS_Y ] ] = 1
        # ゴール地点からスタート地点までの距離を求めたら処理をやめる
        while flag == True:
            # 歩数マップの更新がある限り処理を続ける
            flag = False
            for x in range(self.N):
                for y in range(self.N):
                    if self.distinfo[ x ][ y ] == step:
                        cntr =( x , y )
                        nghbrs = self.neighbor_pos(cntr)[0]
                        # 上下左右マスの歩数マップを更新
                        for dr in range(len(DIRECTION)):
                            if (self.wallinfo[ cntr[ POS_X ] ][cntr[ POS_Y ] ] & DIRECTION[ dr ] ) != DIRECTION[ dr ]:
                                if self.distinfo[ nghbrs[ dr ][ POS_X ] ][ nghbrs[ dr ][ POS_Y ] ] > self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]:
                                    self.distinfo[ nghbrs[ dr ][ POS_X ] ][ nghbrs[ dr ][ POS_Y ] ] = 1 + self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]
                                    flag = True
            step += 1
    def neighbor_pos(self,center):
        chk_flag = [ True, True, True, True ]
        # 引数(center)の上下左右の座標を取得する
        n_right   = ( center[ POS_X ] + 1 , center[ POS_Y ]     )
        n_top     = ( center[ POS_X ]     , center[ POS_Y ] + 1 )
        n_left    = ( center[ POS_X ] - 1 , center[ POS_Y ]     )
        n_bottom  = ( center[ POS_X ]     , center[ POS_Y ] - 1 )
        neighbors = [ n_right , n_top , n_left , n_bottom ]
        for i,chk in enumerate(neighbors):
            if ( chk[ POS_X ] >= self.N ) or ( chk[ POS_Y ] >= self.N ) or ( chk[ POS_X ] <  0 ) or ( chk[ POS_Y ] < 0 ):
                neighbors[ i ] = ( -1, -1)
                chk_flag[ i ] = False
        return neighbors, chk_flag
    def get_nextpos(self, mypos):
        nowwall = self.wallinfo[mypos[POS_X], mypos[POS_Y]]
        nghbrs = self.neighbor_pos(mypos)[0]
        wall = self.wallinfo[nghbrs[1][POS_X]][nghbrs[1][POS_Y]]
        for i in range(4):
            self.n_dist[i] = self.distinfo[nghbrs[i][POS_X]][nghbrs[i][POS_Y]]
            if ( nowwall & DIRECTION[i] ) == DIRECTION[i]:
                self.n_dist[i] = 255
            if ( self.wallinfo[nghbrs[i][POS_X]][nghbrs[i][POS_Y]] & SERCH_COMPLETE ) == SERCH_COMPLETE:
                self.n_dist[i] = 255
        # 四方マスのうち、ゴールまでの距離が同じマスがある場合「右->上->左->下」の順に優先的に選択される
        min_index = self.n_dist.index(min(self.n_dist))
        return nghbrs[min_index]

#-----------------------------------------------------------------------------#
# Function                                                                    #
#-----------------------------------------------------------------------------#
def rev_array(array,size):
    # 配列のxy座標を反転した後に、行を逆転させる(0行目->N行目, 1行目->N-1行目)
    tempinfo = np.array( [ [0] * size] * size )
    for i in range(size):
        for j in range(size):
            tempinfo[ i ][ j ] = array[ j ][ i ]
    tempinfo[ 0 : size ] = tempinfo[ size-1 : : -1 ]
    revarray = tempinfo
    return revarray

def judge_shutdown():
    # タクトスイッチが1秒以上押されていた終了する
    sw_st = mw.switchstate()
    if sw_st[0] == 1:
        # wait 1sec
        time.sleep(1)
        sw_st = mw.switch_state()
        if sw_st[0] == 1:
            # buzz 400Hz sound for 1sec
            mw.buzzer(400)
            time.sleep(1)
            # shutdown
            os.system("/sbin/shutdown -h now")
        else:
            ret = "switch[0] = ON->OFF"
    else:
        ret = "switch[0] = OFF->OFF"
    return ret