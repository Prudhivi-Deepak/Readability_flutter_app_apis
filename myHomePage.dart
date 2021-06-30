import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:readability/info.dart';
import 'results.dart';
import 'package:intl/intl.dart';
import 'package:mysql1/mysql1.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:readability/info.dart';

class MyHomePage1 extends StatelessWidget {
  final FirebaseUser user1;
  MyHomePage1(this.user1);
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Readability')), body: MyHomePage(this.user1));
  }
}

class MyHomePage extends StatefulWidget {
  final FirebaseUser user;

  MyHomePage(this.user);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var decoded1;
  List<String> names = [];
  List<String> names1 = []; 
  String emailvalue="";
  String detect = "";
  String textwarning="";

  String text_data="";
  bool show=false;
  Future<void> predict(user1,text1) async {

        names = ["id", "time","email","text_input","text_standard","automated_readability_index", "coleman_liau_index","crawford", 
                        "dale_chall_readability_score", "difficult_words", "fernandez_huerta", 
                        "flesch_kincaid_grade", "flesch_reading_ease", "gunning_fog", 
                        "gutierrez_polini", "linsear_write_formula", "smog_index", 
                        "szigriszt_pazos"];

        names1 = ["ID", "Date","Email","Text Input","Text Standard","Automated Readability index", "Coleman Liau Index","Crawford", 
                        "Dale Chall Readability Score", "Difficult words", "Fernandez huerta", 
                        "Flesch kincaid grade", "Flesch reading ease", "Gunning fog", 
                        "Gutierrez Polini", "Linsear Write Formula", "Smog Index", 
                        "Szigriszt Pazos"]; 

    final time = DateTime.now();
    final formatter1 = DateFormat(r'''dd/MM/yyyy kk:mm:ss''');
    final String datetime = formatter1.format(time);

    final conn = await MySqlConnection.connect(ConnectionSettings(
        host: 'remotemysql.com', 
        port: 3306,
        user: 'iQnG3ACqz9',
        password: '6reaeX1348',
        db: 'iQnG3ACqz9'
    )); 
    print(user1.email);
    print(datetime);
    print(text1);
    var result = await conn.query('insert into upload (email , time , text_input) values (?,?,?)',[user1.email,datetime,text1]);

    print('Inserted row id=${result.insertId}');
    var ID = '${result.insertId}';
    print(ID);


    final response = await await await http.get(Uri.parse('https://readability-apis.herokuapp.com/'+ID));
    print(response.body);
    decoded1 = json.decode(response.body) as Map<String, dynamic>; 
    print("decoded1-----------------------------------------------------------------------");
    print(decoded1);
    print(decoded1["output"]);

    if(decoded1["output"]=="0"){
      setState(() {
              textwarning="No response Please try again";
            });
    }

    var result1 = await conn.query('insert into predict (id, time,email,text_input,text_standard,automated_readability_index, coleman_liau_index,crawford,dale_chall_readability_score , difficult_words, fernandez_huerta,flesch_kincaid_grade, flesch_reading_ease, gunning_fog,gutierrez_polini, linsear_write_formula, smog_index,szigriszt_pazos) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[decoded1["output"]["id"],decoded1["output"]["time"],decoded1["output"]["email"],decoded1["output"]["text_input"],decoded1["output"]["text_standard"],decoded1["output"]["automated_readability_index"],decoded1["output"]["coleman_liau_index"],decoded1["output"]["crawford"],decoded1["output"]["dale_chall_readability_score"],decoded1["output"]["difficult_words"],decoded1["output"]["fernandez_huerta"],decoded1["output"]["flesch_kincaid_grade"],decoded1["output"]["flesch_reading_ease"],decoded1["output"]["gunning_fog"],decoded1["output"]["gutierrez_polini"],decoded1["output"]["linsear_write_formula"],decoded1["output"]["smog_index"],decoded1["output"]["szigriszt_pazos"]]);

    setState(() {
          show=true;
    });

  }

  void show1() async{
    // ignore: await_only_futures
    emailvalue=widget.user.email;
    print(emailvalue);
    final response = await await await http.get(Uri.parse('https://readability-apis.herokuapp.com/user/'+emailvalue));
    print(response.body);
    decoded1 = json.decode(response.body) as Map<String, dynamic>; 
    print("decoded1-----------------------------------------------------------------------");
    print(decoded1);
    print(decoded1["output"]["0"]);
    var length1= decoded1["output"].length;
    print(length1);
    if(length1==0){
        setState(() {
          detect="There is no such user in database";
        });
      }
      print(emailvalue);
      if(length1!=0){
          setState(() {
            // showing=false;
            Navigator.push(context,
              MaterialPageRoute(builder: (context) => Result(decoded1,length1)));
            print("navigation");
          });
      }
  }

  @override
  Widget build(BuildContext context) {
    return show?Scaffold(
        body:Column(
          mainAxisAlignment:MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
          // Image.network(widget.user.photoUrl,height: 100,width: 400,),
          Text(" Welcome "+widget.user.displayName, style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),),
          Card(
            color: Colors.white,
            child:Padding(padding: EdgeInsets.all(8.0),
                child:TextField(
                minLines: 8,
                maxLines: 8,
                decoration: InputDecoration.collapsed(hintText: "Enter Your Text Here"),
                onChanged: (value)=>text_data=value,
                ),),
          ),
          Column(
              children: <Widget>[
                RaisedButton(
                  onPressed: ()=> this.predict(widget.user,text_data),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                  elevation: 10,
                  splashColor: Colors.redAccent,
                  color: Colors.lightBlue,
                  hoverColor: Colors.green,
                  child: Text("Readability",style: TextStyle(color: Colors.white, fontSize: 25)),
                )
              ]
            ),
            Column(
              children: <Widget>[
                RaisedButton(
                  onPressed: ()=> this.show1(),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                  elevation: 10,
                  splashColor: Colors.redAccent,
                  color: Colors.lightBlue,
                  hoverColor: Colors.green,
                  child: Text("History",style: TextStyle(color: Colors.white, fontSize: 25)),
                )
              ]
          ),
          Column(
              children: <Widget>[
                RaisedButton(
                  onPressed: ()=> print("Improve"),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                  elevation: 10,
                  splashColor: Colors.redAccent,
                  color: Colors.lightBlue,
                  hoverColor: Colors.green,
                  child: Text("Improve",style: TextStyle(color: Colors.white, fontSize: 25)),
                )
              ]
            ),
            Expanded(
              child:Container(
                child:ListView.builder(
                  itemCount: 1,
                  itemBuilder: (context,index){
                  return 
                    Card(
                      child:Container(
                        child:
                          Table(  
                                defaultColumnWidth: FixedColumnWidth(160.0),  
                                // border: TableBorder.all(  
                                //     color: Colors.blueGrey,  
                                //     style: BorderStyle.solid,  
                                //     width: 2),  
                                children: [  
                                  // TableRow(
                                  //   children:[

                                  //     Card(
                                  //       color: Colors.purple[50],
                                  //       child:GestureDetector(
                                  //         onTap: () { 
                                  //             print(names1[0]); 
                                  //             Navigator.push(context,
                                  //                     MaterialPageRoute(builder: (context) => Info(names1[0],0)));
                                  //         },
                                  //         child:Padding(
                                  //           padding: const EdgeInsets.all(8.0),
                                  //             child:Text(names1[0]+" : "+decoded1["output"][names[0]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                  //             ),        
                                  //      ),
                                  //     ),
                                  //      Card(
                                  //       color: Colors.purple[50],
                                  //       child:GestureDetector(
                                  //         onTap: () { 
                                  //             print(names1[1]); 
                                  //              Navigator.push(context,
                                  //                     MaterialPageRoute(builder: (context) => Info(names1[1],1)));
                                  //         },
                                  //         child:Padding(
                                  //           padding: const EdgeInsets.all(8.0),
                                  //             child:Text(names1[1]+" : "+decoded1["output"][names[1]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                  //             ),        
                                  //      ),),
     
                                    
                                  // ]), 

                                  TableRow(
                                    children:[
                                      Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[4]);
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[4],4))); 
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[4]+" : "+decoded1["output"][names[4]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
                                       Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[5]); 
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[5],5)));
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[5]+" : "+decoded1["output"][names[5]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
     
                                    
                                  ]), 

                                  TableRow(
                                    children:[
                                      Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[6]);
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[6],6))); 
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[6]+" : "+decoded1["output"][names[6]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
                                       Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[7]); 
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[7],7)));
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[7]+" : "+decoded1["output"][names[7]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
     
                                    
                                  ]), 

                                  TableRow(
                                    children:[
                                      Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[8]); 
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[8],8)));
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[8]+" : "+decoded1["output"][names[8]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
                                       Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[9]); 
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[9],9)));
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[9]+" : "+decoded1["output"][names[9]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
     
                                    
                                  ]), 

                                  TableRow(
                                    children:[
                                      Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[10]); 
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[10],10)));
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[10]+" : "+decoded1["output"][names[10]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
                                       Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[11]); 
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[11],11)));
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[11]+" : "+decoded1["output"][names[11]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
     
                                    
                                  ]), 

                                  TableRow(
                                    children:[
                                      Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[12]); 
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[12],12)));
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[12]+" : "+decoded1["output"][names[12]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
                                       Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[13]); 
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[13],13)));
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[13]+" : "+decoded1["output"][names[13]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
     
                                    
                                  ]), 

                                  TableRow(
                                    children:[
                                      Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[15]); 
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[15],15)));
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[15]+" : "+decoded1["output"][names[15]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
                                       Card(
                                        color: Colors.purple[50],
                                        child:GestureDetector(
                                          onTap: () { 
                                              print(names1[16]); 
                                               Navigator.push(context,
                                                      MaterialPageRoute(builder: (context) => Info(names1[16],16)));
                                          },
                                          child:Padding(
                                            padding: const EdgeInsets.all(8.0),
                                              child:Text(names1[16]+" : "+decoded1["output"][names[16]].toString(),style: TextStyle(fontSize: 20),textAlign: TextAlign.center,),
                                              ),        
                                       ),),
     
                                    
                                  ]), 

                                 
                                
                    ],  
                  ),
                    ),
                  );
                }
              ))),
    ],))
    : 
    Scaffold(
        body:Column(
          mainAxisAlignment:MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
          // Image.network(widget.user.photoUrl,height: 100,width: 400,),
          Text(" Welcome "+widget.user.displayName, style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),),
          Card(
            color: Colors.white,
            child:Padding(padding: EdgeInsets.all(8.0),
                child:TextField(
                minLines: 8,
                maxLines: 8,
                decoration: InputDecoration.collapsed(hintText: "Enter Your Text Here"),
                onChanged: (value)=>text_data=value,
                ),),
          ),
          Column(
              children: <Widget>[
                RaisedButton(
                  onPressed: ()=> this.predict(widget.user,text_data),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                  elevation: 10,
                  splashColor: Colors.redAccent,
                  color: Colors.lightBlue,
                  hoverColor: Colors.green,
                  child: Text("Readability",style: TextStyle(color: Colors.white, fontSize: 25)),
                )
              ]
            ),
            Column(
              children: <Widget>[
                RaisedButton(
                  onPressed: ()=> this.show1(),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                  elevation: 10,
                  splashColor: Colors.redAccent,
                  color: Colors.lightBlue,
                  hoverColor: Colors.green,
                  child: Text("History",style: TextStyle(color: Colors.white, fontSize: 25)),
                )
              ]
          ),
          Column(
              children: <Widget>[
                RaisedButton(
                  onPressed: ()=> print("Improve"),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                  elevation: 10,
                  splashColor: Colors.redAccent,
                  color: Colors.lightBlue,
                  hoverColor: Colors.green,
                  child: Text("Improve",style: TextStyle(color: Colors.white, fontSize: 25)),
                )
              ]
            ),
            Text(textwarning,style: TextStyle(color: Colors.white, fontSize: 25)),
        ],));
  }
}
