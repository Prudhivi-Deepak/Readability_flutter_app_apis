import 'dart:ffi';

import 'package:flutter/material.dart';

class Result2 extends StatelessWidget {
  int length1;
  var decoded1;
  String email;
  String date;
  Result2(this.decoded1, this.length1,this.email,this.date);

  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Readability')),body: Resultblog2(this.decoded1, this.length1,this.email,this.date));
  }
}

// ignore: must_be_immutable
class Resultblog2 extends StatefulWidget {
  int length1;
  var decoded1;
  String email;
  String date;
  Resultblog2(this.decoded1, this.length1,this.email,this.date);
  @override
  _Resultblog2State createState() => _Resultblog2State();
}

class _Resultblog2State extends State<Resultblog2> {
  var decodedone;
  List<String> names = ["id", "time","email","text_input","text_standard","automated_readability_index", "coleman_liau_index","crawford", 
                        "dale_chall_readability_score", "difficult_words", "fernandez_huerta", 
                        "flesch_kincaid_grade", "flesch_reading_ease", "gunning_fog", 
                        "gutierrez_polini", "linsear_write_formula", "smog_index", 
                        "szigriszt_pazos"];

  List<String> names1 = ["ID", "Date","Email","Text Input","Text Standard","Automated Readability index", "Coleman Liau Index","Crawford", 
                        "Dale Chall Readability Score", "Difficult words", "Fernandez huerta", 
                        "Flesch kincaid grade", "Flesch reading ease", "Gunning fog", 
                        "Gutierrez Polini", "Linsear Write Formula", "Smog Index", 
                        "Szigriszt Pazos"]; 
  List<String> temp=[] ;
  @override
  void initState(){
    super.initState();
    for(var i=0;i<widget.length1;i++){
      if(widget.email==widget.decoded1["output"][i.toString()]["email"] && widget.date==widget.decoded1["output"][i.toString()]["time"]){
        decodedone=widget.decoded1["output"][i.toString()];
        temp.add("1");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return 
    ListView.builder(
                  itemCount: decodedone.length,
                  itemBuilder: (context,index){
                  return 
                    Card(
                      child:ListTile(
                        title: Text(names1[index]+" : "+decodedone[names[index]].toString(),style: TextStyle(fontSize: 20),),
                      ),
                    );
                  }
              );
  }
}