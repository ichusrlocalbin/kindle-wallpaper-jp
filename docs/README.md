# メモ

## バッテリーとの戦い

* [バージョン1](https://github.com/ichusrlocalbin/kindle-wallpaper-jp/commit/020b39f4a9b612b7331b37565a9e787463dd2bea): 何も設定せず → sleepでcronで動作せず、壁紙が更新されない
* [バージョン2](https://github.com/ichusrlocalbin/kindle-wallpaper-jp/commit/5ef6a357a86acd7717f6c81181c3a5dbc92de096): sleepに落ちる直前の `Ready to Suspend` という状態を保つことで、WiFi, cronの動作を維持 → でも、2日くらいしかもたなそう(12時間で30%低下)だった
  * [参考にしたWeb](http://www.mobileread.com/forums/archive/index.php/t-221497.html)
* バージョン3(現バージョン): wifiモジュールをdisableにしてかせぐ
  * [ufuchs/weather-on-kindle4nt](https://github.com/ufuchs/weather-on-kindle4nt/blob/master/weather/bin/platform.sh) の `lipc-set-prop com.lab126.wifid enable 0` `lipc-set-prop com.lab126.wifid enable 1` は動作することは確認した
* バージョン未完: sleepさせて、バッテリーを節約し指定した時刻に起きるように設定 → paperwhiteは出来なさそう。無念。
  * [A remote public service warning display](https://snowtechblog.wordpress.com/2016/02/09/the-kindle-project/) からたどれる [kindle DX用のコード](https://github.com/snowtechblog/avakindle/blob/master/disp_llb.sh) のように`Ready to suspend` のときに、 `lipc-set-prop -i com.lab126.powerd rtcWakeup 60` を設定してみたが、うまく動かず
  * [PW2 Wake up from sleep](http://www.mobileread.com/forums/archive/index.php/t-235821.html) によれば、 paperwhite 2では、 `/sys/class/rtc/rtc1/wakealarm` を使うとsleepからwakeup出来そう。 → papwerwhiteでは× (書き込んでも、値が書き込まれない)

## Livedoor天気予報の画像とKindleに表示する画像の対応表

* [http://weather.livedoor.com/img/icon/8.gif]([http://weather.livedoor.com/img/icon/8.gif]) の数字の部分から、kindleに表示する画像の対応表
* 元々あった画像に無理やり割り当てる(見た目重視)
* そのため、一つの画像に複数の天気が割り当てられている。

|画像ファイル番号|天気|yahoo icon|description|
|----------------|----|----------|-----------|
|1|晴れ|32|sunny|
|2|晴れ時々曇|30|partly cloudy (day)|
|3|晴れ時々雨|40|scattered showers|
|4|晴れ時々雪|16|snow|
|5|晴のち曇|26|cloudy|
|6|晴のち雨|40|scattered showers|
|7|晴のち雪|16|snow|
|8|曇り|28|mostly cloudy (day)|
|9|曇時々晴れ|28|mostly cloudy (day)|
|10|曇時々雨|11|showers|
|11|曇時々雪|16|snow|
|12|曇のち晴れ|28|mostly cloudy (day)|
|13|曇のち雨|11|showers|
|14|曇のち雪|16|snow|
|15|雨|11|showers|
|16|雨時々晴れ|40|scattered showers|
|17|雨時々曇|11|showers|
|18|雨時々雪|5|mixed rain and snow|
|19|雨のち晴れ|40|scattered showers|
|20|雨のち曇|11|showers|
|21|雨のち雪|5|mixed rain and snow|
|22|豪雨|45|thundershowers|
|23|雪|16|snow|
|24|雪時々晴れ|16|snow|
|25|雪時々曇|16|snow|
|26|雪時々雨|16|snow|
|27|雪のち晴れ|16|snow|
|29|雪のち雨|16|snow|
|30|豪雪|16|snow|

### 参考 yahoo.comの対応表

[https://developer.yahoo.com/weather/documentation.html](https://developer.yahoo.com/weather/documentation.html) より

|番号|天気|
|----|----|
|0|tornado|
|1|tropical storm|
|2|hurricane|
|3|severe thunderstorms|
|4|thunderstorms|
|5|mixed rain and snow|
|6|mixed rain and sleet|
|7|mixed snow and sleet|
|8|freezing drizzle|
|9|drizzle|
|10|freezing rain|
|11|showers|
|12|showers|
|13|snow flurries|
|14|light snow showers|
|15|blowing snow|
|16|snow|
|17|hail|
|18|sleet|
|19|dust|
|20|foggy|
|21|haze|
|22|smoky|
|23|blustery|
|24|windy|
|25|cold|
|26|cloudy|
|27|mostly cloudy (night)|
|28|mostly cloudy (day)|
|29|partly cloudy (night)|
|30|partly cloudy (day)|
|31|clear (night)|
|32|sunny|
|33|fair (night)|
|34|fair (day)|
|35|mixed rain and hail|
|36|hot|
|37|isolated thunderstorms|
|38|scattered thunderstorms|
|39|scattered thunderstorms|
|40|scattered showers|
|41|heavy snow|
|42|scattered snow showers|
|43|heavy snow|
|44|partly cloudy|
|45|thundershowers|
|46|snow showers|
|47|isolated thundershowers|
|3200|not available|
