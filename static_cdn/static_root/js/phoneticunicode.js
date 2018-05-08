/**
 * Unicode Phonetic Parser for writing in webpages
 * This script transliterate the user input and display unicode bangla characters
 * 
 * @name Ekushey Unicode Parser
 * @version 1.0 [Date 30th July, 2006]
 * @author Hasin Hayder. Visit My Homepage at http://hasin.wordpress.com
 * @license LGPL
 */
 
/**
 * This script is released under Lesser GNU Public License [LGPL] 
 * which implies that you are free to use this script in your 
 * web applications without any problem. No warranty ensured. If you like 
 * this script, Please acknowledge by keeping a link to my website 
 * http://hasin.wordpress.com in the page where you use this script. 
 */ 
/*
Last Modification:01/11/2008 by Sabuj Kundu(http://manchu.wordpress.com)
Last Modification: 26 Jan 2008 by Omi Azad (http://omi.net.bd)
*/
// Set of Characters
var activeta; //active text area
var phonetic=new Array();

// phonetic bangla equivalents
//Bengali: {U+0980..U+09FF} 
phonetic['k'] = '\u0995'; // ko
//digits
phonetic['0']='\u09e6';//'à§¦'; 
phonetic['1']='\u09e7';//'à§§';
phonetic['2']='\u09e8';//'à§¨';
phonetic['3']='\u09e9';//'à§©';
phonetic['4']='\u09ea';//'à§ª';
phonetic['5']='\u09eb';//'à§«';
phonetic['6']='\u09ec';//'à§¬';
phonetic['7']='\u09ed';//'à§­';
phonetic['8']='\u09ee';//'à§®';
phonetic['9']='\u09ef';//'à§¯';

phonetic['i']='\u09BF'; // hrossho i kar
phonetic['I']='\u0987'; // hrossho i
phonetic['ii']='\u09C0'; // dirgho i kar
phonetic['II']='\u0988'; // dirgho i
phonetic['e']='\u09C7'; // e kar
phonetic['E'] = '\u098F'; // E
phonetic['U'] = '\u0989'; // hrossho u
phonetic['u'] = '\u09C1'; // hrossho u kar
phonetic['uu'] = '\u09C2'; // dirgho u kar
phonetic['UU'] = '\u098A'; // dirgho u
phonetic['r']='\u09B0'; // ro
phonetic['WR']='\u098B'; // wri
phonetic['a']='\u09BE'; // a kar
phonetic['A']='\u0986'; // shore a
phonetic['ao']='\u0985'; // shore o
phonetic['s']='\u09B8'; // dontyo so
phonetic['t']='\u099f'; // to
phonetic['K'] = '\u0996'; // Kho

phonetic['kh'] = '\u0996'; // kho

phonetic['n']='\u09A8'; // dontyo no
phonetic['N']='\u09A3'; // murdhonyo no
phonetic['T']='\u09A4'; // tto
phonetic['Th']='\u09A5'; // ttho

phonetic['d']='\u09A1'; // ddo
phonetic['dh']='\u09A2'; // ddho

phonetic['b']='\u09AC'; // bo
phonetic['bh']='\u09AD'; // bho
phonetic['v']='\u09AD'; // bho
//phonetic['rh']='o';	 // doye bindu ro
phonetic['R']='\u09DC';	 // doye bindu ro
phonetic['Rh']='\u09DD';	 // dhoye bindu ro
phonetic['g']='\u0997';	// go
phonetic['G']='\u0998';	// gho

phonetic['gh']='\u0998'; // gho

phonetic['h']='\u09B9';	// ho
phonetic['NG']='\u099E';	// yo
phonetic['j']='\u099C';	// borgio jo
phonetic['J']='\u099D'; // jho
phonetic['jh']='\u099D'; // jho
phonetic['c']='\u099A'; //  cho
phonetic['ch']='\u099A'; // cho
phonetic['C']='\u099B'; // ccho
phonetic['th']='\u09A0'; // tho
phonetic['p']='\u09AA'; // po
phonetic['f']='\u09AB'; // fo
phonetic['ph']='\u09AB'; // fo
phonetic['D']='\u09A6'; // do
phonetic['Dh']='\u09A7'; // dho

phonetic['z']='\u09AF';// ontoshyo zo
phonetic['y']='\u09DF';	// ontostho yo
phonetic['Ng']='\u0999';	// Uma
phonetic['ng']='\u0982';	// uniswor
phonetic['l']='\u09B2';	// lo
phonetic['m']='\u09AE';	// mo
phonetic['sh']='\u09B6';	// talobyo sho
phonetic['S']='\u09B7'; // mordhonyo sho
phonetic['O']= '\u0993';//'\u09CB'; // o
phonetic['ou']='\u099C'; // ou kar
phonetic['OU']='\u0994'; // OU
phonetic['Ou']='\u0994'; // OU
phonetic['Oi']='\u0990'; // OU
phonetic['OI']='\u0990'; // OU
phonetic['tt']='\u09CE'; // tto
phonetic['H']='\u0983'; // bisworgo
phonetic["."] ="\u0964"; // dari
phonetic[".."] = "."; // fullstop
phonetic['HH'] = '\u09CD' + '\u200c'; // hosonto
phonetic['NN'] = '\u0981'; // chondrobindu
phonetic['Y'] ='\u09CD'+'\u09AF'; // jo fola
phonetic['w'] ='\u09CD'+ '\u09AC'; // wri kar
phonetic['W'] ='\u09C3';// wri kar
phonetic['wr'] ='\u09C3'; // wri kar
phonetic['x'] ="\u0995"  + '\u09CD'+ '\u09B8';
phonetic['rY'] = phonetic['r']+ '\u200D'+ '\u09CD'+'\u09AF';
phonetic['L'] = phonetic['l'];
phonetic['Z'] = phonetic['z'];
phonetic['P'] = phonetic['p'];
phonetic['V'] = phonetic['v'];
phonetic['B'] = phonetic['b'];
phonetic['M'] = phonetic['m'];
phonetic['V'] = phonetic['v'];
phonetic['X'] = phonetic['x'];
phonetic['V'] = phonetic['v'];
phonetic['F'] = phonetic['f'];
//End Set


var carry = '';  //This variable stores each keystrokes
var old_len =0; //This stores length parsed bangla charcter
var ctrlPressed=false;
var len_to_process_oi_kar=0;
var first_letter = false;
var carry2="";
isIE=document.all? 1:0;
var switched=false;

function checkKeyDown(ev)
{
	//just track the control key
	var e = (window.event) ? event.keyCode : ev.which;
	if (e=='17')
	{
		ctrlPressed = true;
	}
}

function checkKeyUp(ev)
{
	//just track the control key
	var e = (window.event) ? event.keyCode : ev.which;
	if (e=='17')
	{
		ctrlPressed = false;
		//alert(ctrlPressed);
	}

}


function parsePhonetic(evnt)
{
	// main phonetic parser
	var t = document.getElementById(activeta); // the active text area
	var e = (window.event) ? event.keyCode : evnt.which; // get the keycode

	if (e=='113')
	{
		//switch the keyboard mode
		if(ctrlPressed){
			switched = !switched;
			//alert("H"+switched);
			return true;
		}
	}

	if (switched) return true;
	
	if(ctrlPressed)
	{
		// user is pressing control, so leave the parsing
		e=0; 
	}

	var char_e = String.fromCharCode(e); // get the character equivalent to this keycode
	
	if(e==8 || e==32)
	{
		// if space is pressed we have to clear the carry. otherwise there will be some malformed conjunctions
		carry = " ";	
		old_len = 1;
		return;
	}

	lastcarry = carry;
	carry += "" + char_e;	 //append the current character pressed to the carry
	
	bangla = parsePhoneticCarry(carry); // get the combined equivalent
	tempBangla = parsePhoneticCarry(char_e); // get the single equivalent

	if (tempBangla == ".." || bangla == "..") //that means it has next sibling
	{
		return false;
	}
	if (char_e=="+")
	{
		if(carry=="++")
		{
			// check if it is a plus sign
			insertJointAtCursor("+",old_len);
			old_len=1;
			return false;
		}	
		//otherwise this is a simple joiner
		insertAtCursor("\u09CD");old_len = 1;
		carry2=carry;
		carry="+";
		return false;
	}
	else if(old_len==0) //first character
	{
		// this is first time someone press a character
		insertJointAtCursor(bangla,1);
		old_len=1;
		return false;
		
	}
/*	else if((char_e=='z' || char_e=='Z')&& carry2=="r+")//force Za-phola after Ra
	{
		//alert('yes');
		insertJointAtCursor('\u200D'+'\u09CD'+phonetic['z'],1);
		old_len=1;	
		return false;
	} */
	else if(carry=="ao")
	{
		// its a shore o
		insertJointAtCursor(parsePhoneticCarry("ao"),old_len);
		old_len=1;
		return false;
	}
	else if (carry == "ii")
	{
		// process dirgho i kar

		insertJointAtCursor(phonetic['ii'],1);
		old_len = 1;
		return false;
	}
	else if (carry == "oi" )
	{
		insertJointAtCursor('\u09C8',1);
		return false;
	}		

	else if (char_e == "o")
	{
		old_len = 1;
		insertAtCursor('\u09CB');
		carry = "o";
		return false;
	}
	else if (carry == "ou")
	{
		// ou kar
		insertJointAtCursor("\u09CC",old_len);
		old_len = 1;
		return false;
	}	
	
	else if((bangla == "" && tempBangla !="")) //that means it has no joint equivalent
	{
		
		// there is no joint equivalent - so show the single equivalent. 
		bangla = tempBangla;
		if (bangla=="")
		{
			// there is no available equivalent - leave as is
			carry ="";
			return;
		}
		
		else
		{
			// found one equivalent
			carry = char_e;
			insertAtCursor(bangla);
			old_len = bangla.length;
			return false;
		}
	}
	else if(bangla!="")//joint equivalent found 
	{
		// we have found some joint equivalent process it
		
		insertJointAtCursor(bangla, old_len);
		old_len = bangla.length;
		return false;
	}
}

    function parsePhoneticCarry(code)
    {
	//this function just returns a bangla equivalent for a given keystroke
	//or a conjunction
	//just read the array - if found then return the bangla eq.
	//otherwise return a null value
        if (!phonetic[code])  //Oh my god :-( no bangla equivalent for this keystroke

        {
			return ''; //return a null value
        }
        else
        {
            return ( phonetic[code]);  //voila - we've found bangla equivalent
        }

    }


function insertAtCursor(myValue) {
	/**
	 * this function inserts a character at the current cursor position in a text area
	 * many thanks to alex king and phpMyAdmin for this cool function
	 * 
	 * This function is originally found in phpMyAdmin package and modified by Hasin Hayder to meet the requirement
	 */
	var myField = document.getElementById(activeta);
	if (document.selection) {		
		myField.focus();
		sel = document.selection.createRange();
		sel.text = myValue;
		sel.collapse(true);
		sel.select();
	}
	//MOZILLA/NETSCAPE support
	else if (myField.selectionStart || myField.selectionStart == 0) {
		
		var startPos = myField.selectionStart;
		var endPos = myField.selectionEnd;
		var scrollTop = myField.scrollTop;
		startPos = (startPos == -1 ? myField.value.length : startPos );
		myField.value = myField.value.substring(0, startPos)
		+ myValue
		+ myField.value.substring(endPos, myField.value.length);
		myField.focus();
		myField.selectionStart = startPos + myValue.length;
		myField.selectionEnd = startPos + myValue.length;
		myField.scrollTop = scrollTop;
	} else {
		var scrollTop = myField.scrollTop;
		myField.value += myValue;
		myField.focus();
		myField.scrollTop = scrollTop;
	}
}

function insertJointAtCursor(myValue, len) {
	/**
	 * this function inserts a conjunction and removes previous single character at the current cursor position in a text area
	 * 
	 * This function is derived from the original one found in phpMyAdmin package and modified by Hasin to meet our need
	 */
	//alert(len);
	var myField = document.getElementById(activeta);
	if (document.selection) {
		myField.focus();
		sel = document.selection.createRange();
		if (myField.value.length >= len){  // here is that first conjunction bug in IE, if you use the > operator
			sel.moveStart('character', -1*(len));   
			//sel.moveEnd('character',-1*(len-1));
		}
		sel.text = myValue;
		sel.collapse(true);
		sel.select();
	}
	//MOZILLA/NETSCAPE support
	else if (myField.selectionStart || myField.selectionStart == 0) {
		myField.focus();
		var startPos = myField.selectionStart-len;
		var endPos = myField.selectionEnd;
		var scrollTop = myField.scrollTop;
		startPos = (startPos == -1 ? myField.value.length : startPos );
		myField.value = myField.value.substring(0, startPos)
		+ myValue
		+ myField.value.substring(endPos, myField.value.length);
		myField.focus();
		myField.selectionStart = startPos + myValue.length;
		myField.selectionEnd = startPos + myValue.length;
		myField.scrollTop = scrollTop;
	} else {
		var scrollTop = myField.scrollTop;
		myField.value += myValue;
		myField.focus();
		myField.scrollTop = scrollTop;
	}
	//document.getElementById("len").innerHTML = len;
}

function makePhoneticEditor(textAreaId)
{
	activeTextAreaInstance = document.getElementById(textAreaId);
	activeTextAreaInstance.onkeypress = parsePhonetic; 
	activeTextAreaInstance.onkeydown = checkKeyDown; 
	activeTextAreaInstance.onkeyup = checkKeyUp;
	activeTextAreaInstance.onfocus = function(){activeta=textAreaId;};
}
function makeVirtualEditor(textAreaId)
{
	activeTextAreaInstance = document.getElementById(textAreaId);
	activeTextAreaInstance.onfocus = function(){activeta=textAreaId;};
}