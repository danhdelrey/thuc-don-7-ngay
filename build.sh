#!/usr/bin/env bash
# Build a tiny APK without Gradle, using the Android SDK on the GitHub runner.
set -euo pipefail
SDK="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}"
[ -n "$SDK" ] || { echo "ANDROID_HOME not set"; exit 1; }
BT="$(ls -d "$SDK"/build-tools/* | sort -V | tail -1)"
PLAT="$SDK/platforms/android-34"
[ -d "$PLAT" ] || PLAT="$(ls -d "$SDK"/platforms/android-* | sort -V | tail -1)"
VC="${VERSION_CODE:-1}"; VN="${VERSION_NAME:-1.0}"
OUT="build"; rm -rf "$OUT"; mkdir -p "$OUT"/{gen,classes,dex}
echo "build-tools: $BT"; echo "platform: $PLAT"

"$BT/aapt2" compile --dir app/res -o "$OUT/res.zip"
"$BT/aapt2" link -o "$OUT/base.apk" -I "$PLAT/android.jar" \
  --manifest app/AndroidManifest.xml -A app/assets --java "$OUT/gen" \
  --min-sdk-version 21 --target-sdk-version 34 \
  --version-code "$VC" --version-name "$VN" "$OUT/res.zip"

javac -source 8 -target 8 -encoding UTF-8 -nowarn -bootclasspath "$PLAT/android.jar" \
  -d "$OUT/classes" $(find app/java "$OUT/gen" -name '*.java')
"$BT/d8" --min-api 21 --release --lib "$PLAT/android.jar" --output "$OUT/dex" \
  $(find "$OUT/classes" -name '*.class')

cp "$OUT/base.apk" "$OUT/unsigned.apk"
(cd "$OUT/dex" && zip -q -X ../unsigned.apk classes.dex)
"$BT/zipalign" -f -p 4 "$OUT/unsigned.apk" "$OUT/aligned.apk"
"$BT/apksigner" sign --ks "$KEYSTORE" --ks-key-alias "$KEY_ALIAS" \
  --ks-pass env:KEYSTORE_PASSWORD --key-pass env:KEYSTORE_PASSWORD \
  --out "$OUT/thuc-don-7-ngay.apk" "$OUT/aligned.apk"
"$BT/apksigner" verify --print-certs "$OUT/thuc-don-7-ngay.apk" | head -3
ls -l "$OUT/thuc-don-7-ngay.apk"
