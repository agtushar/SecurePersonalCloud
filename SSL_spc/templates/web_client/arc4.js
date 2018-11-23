var ARC4 = function(key){
    var s = new Array(256);
    var s2 = new Array(256);

    for (var i = 0; i < 256; i++){
        s[i] = i;
        s2[i] = key.charCodeAt(i % key.length);
    }

    var j = 0;
    for(var i = 0; i < 256; i++){
        j = (j + s[i] + s2[i]) & 0xff;
        var t = s[i];
        s[i] = s[j];
        s[j] = t;
    }

    this.s = s;
}

ARC4.prototype.encrypt = function(message){
    var i = 0;
    var j = 0;
    var encrypted = [];
    var temp = this.s.slice();

    for(var k = 0; k < message.length; k++){
        var charCode = 0;
        i = (i + 1) & 0xff ;
        j = (j + temp[i]) & 0xff;
        var x = temp[i];
        temp[i] = temp[j];
        temp[j] = x;

        if(message.constructor === Array){
            charCode = message[k];
        } else if (message.constructor === String){
            charCode = message.charCodeAt(k);
        }
        encrypted[k] = (charCode ^ temp[(temp[i] + temp[j]) & 0xff]);
    }
    return encrypted;
}

ARC4.prototype.decrypt = function(message){
    return this.encrypt(message);
}

String.prototype.toBuffer = function(string){
    var buff = [];
    for (var i=0; i < this.length; i++) {
        buff[i] = this.charCodeAt(i);
    }
    return buff;
}

Array.prototype.toString = function(){
    var string = '';
    for (var i=0; i < this.length; i++) {
        string += String.fromCharCode(this[i]);
    }
    return string;
}

Array.prototype.isEqualTo = function(array){
    if(this.length !== array.length){
        return false
    }

    for(var i = 0; i < this.length; i++){
        if(this[i] !== array[i]){
            return false;
        }
    }

    return true;
}

// var cipher = new ARC4('Key');
// var buffer = cipher.encrypt('Plaintext');

// console.log("-- Encrypted --");
// console.log(buffer);
// console.log(buffer.toString());

// var otherBuff = cipher.decrypt(buffer)
// console.log("-- Decrypted --");
// console.log(otherBuff);
// console.log(otherBuff.toString());


var test = function (func){
    var testKeys = [
        {
            "key":"Key", "text":"Plaintext", "cipherText":[0xBB, 0xF3, 0x16, 0xE8, 0xD9, 0x40, 0xAF, 0x0A, 0xD3]
        },
        {
            "key":"Wiki", "text":"pedia", "cipherText":[0x10, 0x21, 0xBF, 0x04, 0x020]
        },
        {
            "key":"Secret", "text":"Attack at dawn", "cipherText":[0x45, 0xA0, 0x1F, 0x64, 0x5F, 0xC3, 0x5B, 0x38, 0x35, 0x52, 0x54, 0x4B, 0x9B, 0xF5]
        }
    ];

    for (var i = 0; i < testKeys.length; i++) {
        // Setup
        var cipher = new func(testKeys[i].key);
        var buffer = cipher.encrypt(testKeys[i].text)

        if(buffer.isEqualTo(testKeys[i].cipherText)){
             console.log("Test case: " + (i+1) + " was successful!!");
        } else {
             console.log("Test case: " + (i+1) + " was NOT successful!!");
        }

    }
};

test(ARC4);