// source : https://github.com/locutusjs/locutus/blob/e0a68222d482d43164e96ab96023b712d25680a6/src/php/strings/parse_str.js
function parseString(str, array) {
  var strArr = String(str).replace(/^&/, "").replace(/&$/, "").split("&"),
    sal = strArr.length,
    i,
    j,
    ct,
    p,
    lastObj,
    obj,
    lastIter,
    undef,
    chr,
    tmp,
    key,
    value,
    postLeftBracketPos,
    keys,
    keysLen,
    fixStr = function (str) {
      return decodeURIComponent(str.replace(/\+/g, "%20"));
    };

  for (i = 0; i < sal; i++) {
    tmp = strArr[i].split("=");
    key = fixStr(tmp[0]);
    value = tmp.length < 2 ? "" : fixStr(tmp[1]);
    
    if (key.includes('__proto__') || key.includes('constructor')) {
      console.log('Hmm?')
      break
    }
    while (key.charAt(0) === " ") {
      key = key.slice(1);
    }
    if (key.indexOf("\x00") > -1) {
      key = key.slice(0, key.indexOf("\x00"));
    }
    if (key && key.charAt(0) !== "[") {
      keys = [];
      postLeftBracketPos = 0;
      for (j = 0; j < key.length; j++) {
        if (key.charAt(j) === "[" && !postLeftBracketPos) {
          postLeftBracketPos = j + 1;
        } else if (key.charAt(j) === "]") {
          if (postLeftBracketPos) {
            if (!keys.length) {
              keys.push(key.slice(0, postLeftBracketPos - 1));
            }
            keys.push(key.substr(postLeftBracketPos, j - postLeftBracketPos));
            postLeftBracketPos = 0;
            if (key.charAt(j + 1) !== "[") {
              break;
            }
          }
        }
      }
      if (!keys.length) {
        keys = [key];
      }
      for (j = 0; j < keys[0].length; j++) {
        chr = keys[0].charAt(j);
        if (chr === " " || chr === "." || chr === "[") {
          keys[0] = keys[0].substr(0, j) + "_" + keys[0].substr(j + 1);
        }
        if (chr === "[") {
          break;
        }
      }

      obj = array;
      for (j = 0, keysLen = keys.length; j < keysLen; j++) {
        key = keys[j].replace(/^['"]/, "").replace(/['"]$/, "");
        lastIter = j !== keys.length - 1;
        lastObj = obj;
        if ((key !== "" && key !== " ") || j === 0) {
          if (obj[key] === undef) {
            obj[key] = {};
          }
          obj = obj[key];
        } else {
          // To insert new dimension
          ct = -1;
          for (p in obj) {
            if (obj.hasOwnProperty(p)) {
              if (+p > ct && p.match(/^\d+$/g)) {
                ct = +p;
              }
            }
          }
          key = ct + 1;
        }
      }
      lastObj[key] = value;
    }
  }
}
