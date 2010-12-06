# カラータイル自動求解

## 概要
[カラータイル][]というゲームを自動的に求解しようというプログラムです。
もちろん全消しを狙っています。

## ゲームのルール
23x15の盤面に200個のタイルが並べられます。タイルには10色の色が割り当てられています。これらのタイルを2分間に次のルールに従って消していき、消した個数が点数となります。

* 空マスをクリックする。タイルの存在するマスをクリックしても何も起こらない。
* クリックしたマス目の上下左右のタイルで最も近いタイル（空マスのみを挟んで隣接する）のうちで、同じ色のタイルが2つ以上存在すればそれらを消去し、マスを空マスにする。
* もし空マスをクリックした時に消えるタイルがなければペナルティとして時間が消費される。

## 細かな特徴
### カラーコード
タイルの色のカラーコードです。明るい方はやや怪しいです。
<table>
<tr><th>Color     </th><th>Dark</th>   <th>Light  </th></tr>
<tr><td>Background</td><td><code>#EDEDED</code></td><td><code>#F7F7F7</code></td></tr>
<tr><td>Gray</td>      <td><code>#BBBBBB</code></td><td><code>#D6D6D6</code></td></tr>
<tr><td>Blue</td>      <td><code>#0066FF</code></td><td><code>#5C9DFF</code></td></tr>
<tr><td>Cyan</td>      <td><code>#66CCCC</code></td><td><code>#9DDFDF</code></td></tr>
<tr><td>Green</td>     <td><code>#00CC00</code></td><td><code>#63E063</code></td></tr>
<tr><td>Yellow</td>    <td><code>#CCCC66</code></td><td><code>#DFDFA0</code></td></tr>
<tr><td>Brown</td>     <td><code>#CC6600</code></td><td><code>#E0A366</code></td></tr>
<tr><td>Orange</td>    <td><code>#FF9900</code></td><td><code>#FFC260</code></td></tr>
<tr><td>Red</td>       <td><code>#FF6666</code></td><td><code>#FFA3A3</code></td></tr>
<tr><td>Pink</td>      <td><code>#FF88FF</code></td><td><code>#FFB4FF</code></td></tr>
<tr><td>Magenta</td>   <td><code>#CC66CC</code></td><td><code>#E0A3E0</code></td></tr>
</table>

### 色の判別
暫定的に色の判別方法を決定する。色のRGB値をそれぞれR,G,Bで表現する。

1. R=G=B なら`#E0E0E0`以下か以上かで*gray*か*empty*かを判定する。
2. R<G<B なら*blue*
3. R<G=B なら*cyan*
4. B=R<G なら*green*
5. B<R=G なら*yellow*
6. R>G>B ならRが`0xff`のときは*orange*で、それ以外は*brown*と判定。
   あるいは、Gが`0xbb`以上なら*orange*で、それ以外は*brown*とか。
7. R>G=B なら*red*
8. G<B=R ならRが`0xff`のときは*pink*で、それ以外は*magenta*と判定。

[カラータイル]: http://www.gamesaien.com/game/color_tiles/
