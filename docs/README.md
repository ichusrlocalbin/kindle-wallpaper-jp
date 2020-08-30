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

