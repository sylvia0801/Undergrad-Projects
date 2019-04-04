const util = require('util')
var promise = require('bluebird')
var http = require('http')

var questions = require('./questions.js').questions

var mongodb = promise.promisifyAll(require('mongodb'))

var mongoURL = 'mongodb://localhost:27017/database'

var onlineFindHost = 'www.webservicex.net'
var onlineFindPath = '/stockquote.asmx/GetQuote?symbol='

var mainController = {
    username:"",
    object:"mainController", 
    title:"Search For Ticker", 
    currentTicker:{ 
        Symbol:""
    },
    quizQuestion:10,
    currentQuestion: questions[0],
    question: questions[0].question,
    totalScore: 0,
    answers: Object.keys(questions[0].answers)
};


function parseResult(result){
    var text = result.replace(/&gt;/g,"").replace(/&lt;/g,"");
    //var arr = text.split("Symbol")

    var info = {"":""}
    function isolate(seperator) {
        var arr = text.split(seperator);
        
        if (arr.length >= 2){
            var value = arr[1].replace(" /","");
            info[seperator] = value.substring(0,value.length - 1);
            console.log("in parse" + seperator + info[seperator])
        } else {
            info[""] = "";
        }
    }
    
    isolate("Symbol");
    isolate("Last");
    isolate("Date");
    isolate("Time");
    isolate("Change");
    isolate("Open");
    isolate("High");
    isolate("Low");
    isolate("Volume");
    isolate("MktCap");
    isolate("PreviousClose");
    isolate("PercentageChange");
    isolate("AnnRange");
    isolate("Earns");
    isolate("P-E");
    isolate("Name");
    
    return info;

};

mainController.findTickerOnline = function (ticker){
    var options = {
      host: onlineFindHost,
      path: onlineFindPath + ticker
    };
    
    return new Promise(function (resolve, reject) {
        var content = ""; 
      

        var request = http.request(options, function(res) {
            res.setEncoding("utf8");
            res.on("data", function (chunk) {
                content += chunk;
            });

            res.on("end", function () {
                
                
                parsedContent = parseResult(content);
                console.log("HEREE:" + util.inspect(parsedContent));
                resolve(parsedContent);
            });
        })
        .on('error', function (err){
            reject(err)
        });
    

        request.end();
    });
    
    
};

mainController.processSymbol = function (ticker, renderCB){
    
    mongodb.MongoClient.connect(mongoURL)
    .then(function (db){
        db
        .collection('tickers')
        .find({'Symbol' : ticker})
        .toArray()
        .then(function(data){
            if (data.length){
                currentTicker = data[0];
                renderCB(data[0]);
                db.close()
            }
            else{
                db.close();
                
                mainController.findTickerOnline(ticker)
                .then(function(data){
                    currentTicker = data;
                        
                    mongodb.MongoClient.connect(mongoURL)
                    .then(function (db){
                        db
                        .collection('tickers')
                        .insert([data])
                        .then(function(){
                            renderCB(data);
                            db.close();
                        }); 
                    })
                    .catch(function (err){
                        console.log('error in storing data:' + err);
                    });
                })
                .catch(function (err){
                    console.log('suberror ' + err);
                });
            }
        })
        .catch(function(err) {
            db.close
            console.log("error:" + err)
        });       
    })
    .catch(function(err) {
        console.error("ERROR", err);
    });
    console.log("Processed symbol");
};

mainController.recieveUserInput = function (val){
    //quiz question 10 to account for how old are you question (i.e 30,31,32)
        
    if (0 == this.quizQuestion){
        this.answers = Object.keys({
            "Over 60" : "0",
            "50-59" : "1",
            "40-49" : "2",
            "30-39" : "3",
            "Under 29" : "4"
        });
        this.question = "What is your current age?";
        
        this.quizQuestion += 10;
        
    }
    else if (20 == this.quizQuestion){
        /*[
            {
                "Below 45":{
                    "Over $250,000":"2",
                    "$100 - $250,000":"3",
                    "$0 - $99,000":"4"
                },
                "45 or Above":{
                    "Over $1000":"0",
                    "$500 - $1,000,000":"1",
                    "Under $500,000":"2"
                }
            }
        ]*/
        this.answers = Object.keys(questions[2].answers);
        this.question = "How old are you?";
        
        this.quizQuestion += 10;
        this.totalScore += val;
        
    }
    else if (30 == this.quizQuestion){
        this.answers = Object.keys(questions[2].answers[val]);
        this.question = "What is the approximate value of your current combined retirement savings?";
        
        this.quizQuestion += val + 1;
    }
    else if (31 == this.quizQuestion || 32 == this.quizQuestion){
        this.answers = Object.keys(questions[3].answers);
        this.question = questions[3].question;
        this.totalScore += val;
        this.quizQuestion == 40;
    }
    else {
        this.answers = Object.keys(questions[this.quizQuestion/10]);
        this.question = questions[this.quizQuestion/10];
        
        this.quizQuestion += 10;
        this.totalScore += val;
    }
};

module.exports.mainController = mainController;