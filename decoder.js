#!/usr/bin/env node
console.log("test");

var letters = 'a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9 ! ?'.split(' ');
console.log(letters);
console.log(letters.indexOf('n'));
console.log(letters.indexOf('D'));
var decodeMove = function(move) {
        if (move.length != 2) throw "Invalid Move: " + move;
        var m1 = move.substring(0, 1);
        var m2 = move.substring(1, 2);
	console.log('m1:', m1);
	console.log('m2:', m2);
        var p1 = letters.indexOf(m1);
	console.log('p1:', p1);
        var p2 = letters.indexOf(m2);
	console.log('p2:', p2);
        var remainder1 = p1 % 8;
        var remainder2 = p2 % 8;
        var quotient1 = parseInt(p1 / 8);
        var quotient2 = parseInt(p2 / 8);
        var movePosition_START_X = letters[remainder1];
        var movePosition_START_Y = quotient1 + 1;
        var movePosition_END_X = letters[remainder2];
        var movePosition_END_Y = quotient2 + 1;
        var pos = String(movePosition_START_X) + String(movePosition_START_Y) + String(movePosition_END_X) + String(movePosition_END_Y);
	console.log('pos:', pos);
    };

var m = 'nD';
decodeMove(m);
m = 'ZJ';
decodeMove(m);

