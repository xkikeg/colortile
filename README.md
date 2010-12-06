# カラータイル自動求解

## 概要
カラータイルというゲームを自動的に求解しようというプログラムです。
もちろん全消しを狙っています。

## ゲームのルール
23x15の盤面に200個の石が並べられます。石には9色の色が割り当てられています。
これらの石を2分間に次のルールに従って消していき、消した個数が点数となります。

* 空マスをクリックする。石の存在するマスをクリックしても何も起こらない。
* クリックしたマス目の上下左右の石で最も近い石（空マスのみを挟んで隣接する）の
  うちで、同じ色の石が2つ以上存在すればそれらを消去し、マスを空マスにする。
* もし空マスをクリックした時に消える石がなければペナルティとして時間が消費され
  る。

## 細かな特徴
### カラーコード
石の色のカラーコードです。明るい方はやや怪しいです。
<table>
<tr><td rowspan="2">Bg</td>     <td>dark</td> <td>#EDEDED</td></tr>
<tr>                            <td>light</td><td>#F7F7F7</td></tr>
<tr><td rowspan="2">Gray</td>   <td>dark</td> <td>#BBBBBB</td></tr>
<tr>                            <td>light</td><td>#D6D6D6</td></tr>
<tr><td rowspan="2">Blue</td>   <td>dark</td> <td>#0066FF</td></tr>
<tr>                            <td>light</td><td>#5C9DFF</td></tr>
<tr><td rowspan="2">Cyan</td>   <td>dark</td> <td>#66CCCC</td></tr>
<tr>                            <td>light</td><td>#9DDFDF</td></tr>
<tr><td rowspan="2">Green</td>  <td>dark</td> <td>#00CC00</td></tr>
<tr>                            <td>light</td><td>#63E063</td></tr>
<tr><td rowspan="2">Yellow</td> <td>dark</td> <td>#CCCC66</td></tr>
<tr>                            <td>light</td><td>#DFDFA0</td></tr>
<tr><td rowspan="2">Brown</td>  <td>dark</td> <td>#CC6600</td></tr>
<tr>                            <td>light</td><td>#E0A366</td></tr>
<tr><td rowspan="2">Orange</td> <td>dark</td> <td>#FF9900</td></tr>
<tr>                            <td>light</td><td>#FFC260</td></tr>
<tr><td rowspan="2">Pink</td>   <td>dark</td> <td>#FF6666</td></tr>
<tr>                            <td>light</td><td>#FFA3A3</td></tr>
<tr><td rowspan="2">Magenta</td><td>dark</td> <td>#CC66CC</td></tr>
<tr>                            <td>light</td><td>#E0A3E0</td></tr>
</table>
