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
goal  = ( ( 7 , 7 ) , ( 7 , 8 ) ,  ( 8 , 7 ) , ( 8 , 8 ) )
#goal  = ( ( 2 , 11 ) , ( 2 , 12 ) ,  ( 3 , 11 ) , ( 3 , 12 ) )
route = (  6 , 8 )
#route = (  9 , 8 )
#route = (  4 , 11 )
#route = ( 7 , 6 )
# 壁情報のビット表現
RIGHT  = 0b00000001
TOP    = 0b00000010
LEFT   = 0b00000100
BOTTOM = 0b00001000
SERCH_COMPLETE     = 0b00010000
SERCH_NOT_COMPLETE = 0b00000000
DIRECTION = [ RIGHT, TOP, LEFT, BOTTOM ]
# 配列内の要素番号の意味を分かりやすくするための宣言
POS_X  = 0
POS_Y  = 1

#-----------------------------------------------------------------------------#
# Class                                                                       #
#-----------------------------------------------------------------------------#
# 迷路クラス
class Maze:
    def __init__( self ):
        # wallinfo[ x ][ y ]
        #  0bit: 0 = 右に壁なし, 1 = 右に壁あり
        #  1bit: 0 = 上に壁なし, 1 = 上に壁あり
        #  2bit: 0 = 左に壁なし, 1 = 左に壁あり
        #  3bit: 0 = 下に壁なし, 1 = 下に壁あり
        #  4bit: 0 = マスの探索未完了, 1 = マスの探索完了
        self.N = 16
        self.minstep = 1
        self.n_dist = [ 0, 0, 0, 0 ]
        # 壁情報を数字の0で初期化する
        self.wallinfo = np.array( [ [ 0 ] * self.N ] * self.N )
        #for pos in goal:
        #    self.wallinfo[ pos[ POS_X ] ][ pos[ POS_Y ] ] = 255
        self.wallinfo[ route[ POS_X ] ][ route[ POS_Y ] ] = 0
        # distinfo[ x ][ y ]
        #  0 ～ 255で距離情報を表す
        # 距離情報を数字の255で初期化する
        self.distinfo = np.array( [ [ 255 ] * self.N ] * self.N )
        self.distinfo[ start[ POS_X ]  ][ start[ POS_Y ]  ] = 255
        #for pos in goal:
        #    self.distinfo[ pos[ POS_X ] ][ pos[ POS_Y ] ] = 255
        self.distinfo[ route[ POS_X ] ][ route[ POS_Y ] ] = 1
    def get_wallinfo( self ):
        # 現時点で判明している壁情報を取得する
        # 返り値
        #   wallinfo : 全座標の距離情報を格納したリスト
        return self.wallinfo
    def set_wallinfo( self, set_pos, new_wallinfo ):
        # 壁情報を更新
        # 引数
        #   set_pos : 壁情報を更新したい(x,y)座標。2要素を持つリスト形式かタプル形式で指定。
        #   new_wallinfo : 更新する壁情報の値
        self.wallinfo[ set_pos[ POS_X ] ][ set_pos[ POS_Y ] ] |= ( 0b00001111 & new_wallinfo )
        wallinfo =  self.wallinfo[ set_pos[ POS_X ] ][ set_pos[ POS_Y ] ]
        nghbrs, chk = self.neighbor_pos( set_pos )
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
    def display_wallinfo( self ):
        # 地図情報をコマンドラインに表示する
        tempinfo = self.wallinfo
        tempinfo = rev_array( tempinfo, self.N )
        print "wallinfo = "
        print tempinfo  & 0b11101111
    def get_distinfo( self ):
        # 現時点で判明している距離情報を取得する
        # 返り値
        #  distinfo : 全座標の距離情報を格納したリスト
        return self.distinfo
    def set_distinfo( self, set_pos, new_distinfo ):
        # 距離情報を更新する
        # 引数
        #   set_pos : 壁情報を更新したい(x,y)座標。2要素を持つリスト形式かタプル形式で指定。
        #   new_distinfo : 更新する距離情報の値
        self.distinfo[ set_pos[0] ][ set_pos[ POS_Y ] ]  = new_distinfo
    def display_distinfo( self ):
        # 距離情報をコマンドラインに表示する
        tempinfo = self.distinfo
        tempinfo = rev_array( tempinfo, self.N )
        print "distinfo = "
        print tempinfo
    def adachi( self ):
        # 足立法で各マスの距離情報を取得する
        step = self.minstep
        flag = True
        self.distinfo = np.array( [ [ 255 ] * self.N ] * self.N )
        self.distinfo[ route[ POS_X ] ][ route[ POS_Y ] ] = 1
        # ゴール地点からスタート地点までの距離を求めたら処理をやめる
        while flag == True:
            # 歩数マップの更新がある限り処理を続ける
            flag = False
            for x in range( self.N ):
                for y in range( self.N ):
                    if self.distinfo[ x ][ y ] == step:
                        cntr =( x , y )
                        nghbrs = self.neighbor_pos( cntr )[ 0 ]
                        # 上下左右マスの歩数マップを更新
                        for dr in range( len( DIRECTION ) ):
                            if (self.wallinfo[ cntr[ POS_X ] ][cntr[ POS_Y ] ] & DIRECTION[ dr ] ) != DIRECTION[ dr ]:
                                if self.distinfo[ nghbrs[ dr ][ POS_X ] ][ nghbrs[ dr ][ POS_Y ] ] > self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]:
                                    self.distinfo[ nghbrs[ dr ][ POS_X ] ][ nghbrs[ dr ][ POS_Y ] ] = 1 + self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]
                                    flag = True
            step += 1
    def adachi_2nd_run( self ):
        # 足立法で各マスの距離情報を取得する
        step = self.minstep
        flag = True
        self.distinfo = np.array( [ [ 255 ] * self.N ] * self.N )
        self.distinfo[ route[ POS_X ] ][ route[ POS_Y ] ] = 1
        # ゴール地点からスタート地点までの距離を求めたら処理をやめる
        while flag == True:
            # 歩数マップの更新がある限り処理を続ける
            flag = False
            for x in range( self.N ):
                for y in range( self.N ):
                    if self.distinfo[ x ][ y ] == step:
                        cntr =( x , y )
                        nghbrs = self.neighbor_pos( cntr )[ 0 ]
                        # 上下左右マスの歩数マップを更新
                        for dr in range( len( DIRECTION ) ):
                            if (self.wallinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ] & DIRECTION[ dr ] ) != DIRECTION[ dr ]:
                                if ( ( self.wallinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ] & SERCH_COMPLETE ) == ( SERCH_COMPLETE )  ) and ( self.distinfo[ nghbrs[ dr ][ POS_X ] ][ nghbrs[ dr ][ POS_Y ] ] > self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ] ):
                                    self.distinfo[ nghbrs[ dr ][ POS_X ] ][ nghbrs[ dr ][ POS_Y ] ] = 1 + self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]
                                    flag = True
            step += 1
    def neighbor_pos( self, center ):
        # 引数(center)の上下左右の座標を取得する
        # 引数
        #   center : (x,y)座標。2要素を持つリスト形式かタプル形式で指定。
        # 返り値
        #   neighbors : center の上下左右の座標を表す(x,y)座標が4個含まれるリスト。
        #   chk_flg : center の上下左右座標が壁の向こうを表していたらFalseを返す4要素のリスト。
        chk_flag = [ True, True, True, True ]
        n_right   = ( center[ POS_X ] + 1 , center[ POS_Y ]     )
        n_top     = ( center[ POS_X ]     , center[ POS_Y ] + 1 )
        n_left    = ( center[ POS_X ] - 1 , center[ POS_Y ]     )
        n_bottom  = ( center[ POS_X ]     , center[ POS_Y ] - 1 )
        neighbors = [ n_right , n_top , n_left , n_bottom ]
        for i,chk in enumerate( neighbors ):
            if ( chk[ POS_X ] >= self.N ) or ( chk[ POS_Y ] >= self.N ) or ( chk[ POS_X ] <  0 ) or ( chk[ POS_Y ] < 0 ):
                neighbors[ i ] = center
                chk_flag[ i ] = False
        return neighbors, chk_flag
    def get_nextpos( self, mypos ):
        # 距離情報を元に、次に進むマスを決める
        # 探索済のマスがある方向に進まないようになっているので、1回目の走行用
        # 引数
        #   mypos : 現在地を表す(x,y)座標のリストもしくはタプル。
        # 返り値
        #   nextpos : 次に進むべきマスの(x,y)座標のリスト
        nextpos = [ 0 , 0 ]
        nghbrs = self.neighbor_pos( mypos )[ 0 ]
        nowwall = self.wallinfo[ mypos[ POS_X ], mypos[ POS_Y ] ]
        for i in range( 4 ):
            # 上下左右マスに壁がある場合はゴールに向かう
            if mypos in goal:
                nextpos = mypos
                break
            else:
                self.n_dist[ i ] = self.distinfo[ nghbrs[ i ][ POS_X ] ][ nghbrs[ i ][ POS_Y ] ]
                if ( nowwall & DIRECTION[ i ] ) == DIRECTION[ i ]:
                    # 壁がある場合はその方向に進まないようにする
                    # ( min関数でindexが選ばれないようにするために255を代入 )
                    self.n_dist[ i ] = 255
                else: 
                    if nghbrs[ i ] in goal:
                        nextpos = nghbrs[ i ]
                        break
                # 四方マスのうち、ゴールまでの距離が同じマスがある場合「右->上->左->下」の順に優先的に選択される
                min_index = self.n_dist.index( min( self.n_dist ) )
                nextpos = nghbrs[ min_index ]
        return nextpos

#-----------------------------------------------------------------------------#
# Function                                                                    #
#-----------------------------------------------------------------------------#
def rev_array( array, size ):
    # 配列のxy座標を反転した後に、行を逆転させる(0行目->N行目, 1行目->N-1行目)
    tempinfo = np.array( [ [ 0 ] * size ] * size )
    for i in range( size ):
        for j in range( size ):
            tempinfo[ i ][ j ] = array[ j ][ i ]
    tempinfo[ 0 : size ] = tempinfo[ size-1 : : -1 ]
    revarray = tempinfo
    return revarray

def judge_shutdown():
    # タクトスイッチが1秒以上押されていた終了する
    sw_st = mw.switchstate()
    if sw_st[ 0 ] == 1:
        # wait 1sec
        time.sleep( 1 )
        sw_st = mw.switch_state()
        if sw_st[ 0 ] == 1:
            # buzz 400Hz sound for 1sec
            mw.buzzer( 400 )
            time.sleep( 1 )
            # shutdown
            os.system("/sbin/shutdown -h now")
        else:
            ret = "switch[ 0 ] = ON->OFF"
    else:
        ret = "switch[ 0 ] = OFF->OFF"
    return ret
