import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';
class Info extends StatelessWidget {
  String name;
  int i;
  Info(this.name, this.i);
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Readability')), body: Info1(this.name,this.i));
  }
}

class Info1 extends StatefulWidget {
  String name;
  int i;
  Info1(this.name,this.i);
  
  @override
  _Info1State createState() => _Info1State();
}

class _Info1State extends State<Info1> {

  List<String> textinfo = ["This is the id of the input","This is the todays date","","","Based upon all the Other tests, returns the estimated school grade level required to understand the text"
                          ,"The automated readability index is a readability test designed to measure the how easy your text is to understand."
                            ,"Coleman and Liau developed the formula to automatically calculate writing samples instead of manually coding the text."
                            ,"Returns an estimate of the years of schooling required to understand the text. The text is only valid for elementary school level texts."
                            ,"Different from other tests, since it uses a lookup table of the most commonly used 3000 English words. Thus it returns the grade level using the New Dale-Chall Formula."
                            ,"Difficult words are found by using all other metrics calculated."
                            ,"The Huerta score* was an adaptation of the Flesch Reading Ease score intoSpanish. The Flesch formula for English text, first published in 1948, is : Flesch = 206.835 - 84.6 * syllables/words - 1.015 * words/sentences"
                            ,"Returns the Flesch-Kincaid Grade of the given text. This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document."
                            ,"The Flesch Reading Ease Formula is a simple approach to assess the grade-level of the reader."
                            ,"The index estimates the years of formal education a person needs to understand the text on the first reading."
                            ,"","The result is a grade level measure, reflecting the estimated years of education needed to read the text fluently."
                            ,"The SMOG grade is a measure of readability that estimates the years of education needed to understand a piece of writing. "
                            ];
  
List<String> formulas =  ["","","","",""
                          ,"Automated Readability Index formula: 4.71 x (characters/words) + 0.5 x (words/sentences) - 21.43."
                            ,"Coleman Liau Index formula: 5.89 x (characters/words) - 0.3 x (sentences/words) – 15.8."
                            ,"A = -0.205OP+0.049SP - 3.407. A is the number of years of schooling; OP , the number of sentences per hundred words; SP , the number of syllables per hundred words. The result is rounded to the nearest tenth."
                            ,"The formula for calculating the raw score of the Dale–Chall readability score (1948) is =0.1579((difficultwords/words)100)+0.0496(words/sentences)"
                            ,"It may check in the library of commomly used words it Has . "
                            ,"The Huerta formula is usually presented as 206.84 - (0.60 * P) - (1.02 *F), where P = number of syllables and F = number of sentences, as countedin a sample containing 100 words"
                            ,"Flesch-Kincaid grade level formula: 0.39 x (words/sentences) + 11.8 x (syllables/words) - 15.59."
                            ," RE = 206.835 – (1.015 x ASL) – (84.6 x ASW) RE = Readability Ease ASL = Average Sentence Length (i.e., the number of words divided by the number of sentences)ASW = Average number of syllables per word (i.e., the number of syllables divided by the number of words)"
                            ,"Gunning fog index = 0.4[(words/sentences)+100(complex words/eords)]"
                            ,"","For each easy word, defined as words with 2 syllables or less, add 1 point.For each hard word, defined as words with 3 syllables or more, add 3 points.Divide the points by the number of sentences in the 100-word sample.Adjust the provisional result r : If r > 20, Lw = r / 2.If r ≤ 20, Lw = r / 2 - 1"
                            ,"Grade=1.0430[sqrt((number of polysyllables)(30/number of sentences))]+3.1291"

                            ];

List<String> ref =  ["","","","",""
                          ,"https://www.webfx.com/tools/read-able/automated-readability-index.html"
                            ,"https://www.webfx.com/tools/read-able/coleman-liau-index.html"
                            ,"https://legible.es/blog/formula-de-crawford/"
                            ,"https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula"
                            ,""
                            ,"https://linguistlist.org/issues/22/22-2332/"
                            ,"https://www.webfx.com/tools/read-able/flesch-kincaid.html"
                            ,"https://readabilityformulas.com/flesch-reading-ease-readability-formula.php"
                            ,"https://en.wikipedia.org/wiki/Gunning_fog_index"
                            ,"","https://en.wikipedia.org/wiki/Linsear_Write"
                            ,"https://en.wikipedia.org/wiki/SMOG"
                            ];

List<String> images =  ["","","","",""
                          ,"ARI.png"
                            ,"CLI.png"
                            ,"cra.png"
                            ,"dale.png"
                            ,""
                            ,"hue.png"
                            ,"fleasch.png"
                            ,"fleash.png"
                            ,"gun.png"
                            ,"","linear.png"
                            ,"smog.png"
                            ];                      

                          
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
          mainAxisAlignment:MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          SizedBox(height: 10,),
          Expanded(
            child:ListView.builder(
                  itemCount: 1,
                  itemBuilder: (context,index){
                  return Card(
                    margin: EdgeInsets.all(5),
                    color: Colors.lightBlueAccent,
                    child: Column(
                      
                    children: [
                    SizedBox(height: 10,),
                    Text(widget.name,style: TextStyle(color: Colors.black, fontSize: 30,fontWeight: FontWeight.bold),textAlign:TextAlign.center,),
                    SizedBox(height: 10,),
                    Text(textinfo[widget.i],style: TextStyle(color: Colors.black, fontSize: 25),textAlign:TextAlign.left,),
                    SizedBox(height: 10,),
                  ],)
                  ,);
                  }
            )
          ),
          SizedBox(height: 10,),
          formulas[widget.i]!=""?Expanded(
            child:ListView.builder(
                  itemCount: 1,
                  itemBuilder: (context,index){
                  return Card(
                    color: Colors.lightGreenAccent,
                    child: Column(
                    children: [
                    SizedBox(height: 10,),
                    Text("Calculation",style: TextStyle(color: Colors.black, fontSize: 30,fontWeight: FontWeight.bold),textAlign:TextAlign.center,),
                    SizedBox(height: 10,),
                    Text(formulas[widget.i],style: TextStyle(color: Colors.black, fontSize: 20),textAlign:TextAlign.left,),
                    SizedBox(height: 10,),
                  ],)
                  ,);
                  }
            )
          )
          :Text(""),
          SizedBox(height: 10,),
          images[widget.i]!=""?Expanded(
            child:ListView.builder(
                  itemCount: 1,
                  itemBuilder: (context,index){
                  return Card(
                    color: Colors.deepOrange,
                    child: Column(
                    children: [
                    SizedBox(height: 10,),
                    Text("Formula",style: TextStyle(color: Colors.black, fontSize: 30,fontWeight: FontWeight.bold),textAlign:TextAlign.center,),
                    SizedBox(height: 10,),
                    Image.asset('assets/'+images[widget.i],height: 100,width: 400,),
                    SizedBox(height: 10,),
                  ],)
                  ,);
                  }
            )
          )        
          :Text(""),
          SizedBox(height: 10,),
          ref[widget.i]!=""?Expanded(
            child:ListView.builder(
                  itemCount: 1,
                  itemBuilder: (context,index){
                  return Card(
                    color: Colors.blueGrey,
                    child: Column(
                    children: [
                    SizedBox(height: 10,),
                    Text("References",style: TextStyle(color: Colors.black, fontSize: 30,fontWeight: FontWeight.bold),textAlign:TextAlign.center,),
                    SizedBox(height: 10,),
                    InkWell(              
                        child: new Text(widget.name,style: TextStyle(color: Colors.black, fontSize: 20),textAlign:TextAlign.center,),
                        onTap: () => launch(ref[widget.i])
                    ),
                    SizedBox(height: 10,),
                  ],)
                  ,);
                  }
            )
          )
          :Text(""),

        ],
      ),
    );
  }
}
