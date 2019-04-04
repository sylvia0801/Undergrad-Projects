var express = require('express');
var router = express.Router();
var mainController = require('../public/javascripts/mainController.js').mainController
var questions = require('../public/javascripts/questions.js').questions
const util = require('util')

/* GET home page. */

router.get('/', function(req, res, next) {
    //mainController.answers = Object.keys(questions[0].answers);
    //mainController.question = questions[0].question;
    
    mainController.answers = [
            "Over 60",
            "50-59",
            "40-49",
            "30-39",
            "Under 29" 
        ]
    mainController.question = "What is your current age?";
    
    mainController.image = "";
        
    mainController.processSymbol('GOOG', function(data){
        mainController.symbol = data['Symbol'];
        res.render('index', { "data":{"tickerInfo":data, 
                                      "currentQuestion": mainController.question, 
                                      "currentAnswers":mainController.answers,
                                      "image":mainController.image,
                                      "username":mainController.username}
                            });
        
    });
});

router.post('/', function(req, res, next) {
    
    var ticker = req.body.tickerInput;
    
    mainController.processSymbol(ticker, function(data){
        mainController.symbol = data['Symbol'];
        res.render('index', { "data":{"tickerInfo":data, 
                                      "currentQuestion": mainController.question, 
                                      "currentAnswers":mainController.answers,
                                      "image":mainController.image,
                                      "username":mainController.username}
                            });
        
    });
    
});

router.post('/response', function(req, res, next) {
    
    var ticker = mainController.symbol;
    
    console.log('here');
    
    recieveInfo(req.body.options,function(ticker){
    
        mainController.processSymbol(ticker, function(data){
            mainController.symbol = data['Symbol'];
            res.render('index', { "data":{"tickerInfo":data, 
                                          "currentQuestion": mainController.question, 
                                          "currentAnswers":mainController.answers,
                                          "image":mainController.image,
                                          "username":mainController.username}
                                });
        });
    })  
});

router.post('/login', function(req, res, next){
    
    var username = req.body.username;
    mainController.username = username;
    
    mainController.processSymbol(mainController.symbol, function(data){
            mainController.symbol = data['Symbol'];
            res.render('index', { "data":{"tickerInfo":data, 
                                          "currentQuestion": mainController.question, 
                                          "currentAnswers":mainController.answers,
                                          "image":mainController.image,
                                          "username":mainController.username}
                                });
        });
});

router.post('/logout', function(req, res, next){
    
    var username = req.body.username;
    mainController.username = "";
    
    mainController.processSymbol(mainController.symbol, function(data){
            mainController.symbol = data['Symbol'];
            res.render('index', { "data":{"tickerInfo":data, 
                                          "currentQuestion": mainController.question, 
                                          "currentAnswers":mainController.answers,
                                          "image":mainController.image,
                                          "username":mainController.username}
                                });
        });
});

var recieveInfo = function (val,cb){
    
    console.log("Value: " + val + " total:" + mainController.totalScore);
    
    var processSymbol = cb
    //quiz question 10 to account for how old are you question (i.e 30,31,32)
    //console.log("ekko" + mainController.quizQuestion)
    if (20 == mainController.quizQuestion){
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
        mainController.answers = Object.keys(questions[2].answers[0]);
        mainController.question = "How old are you?";
        
        mainController.quizQuestion += 10;
        mainController.totalScore += parseInt(val);
        
        processSymbol(mainController.symbol);
    }
    else if (30 == mainController.quizQuestion){
        var howOld = Object.keys(questions[2].answers[0])[parseInt(val)];
        
        mainController.answers = Object.keys(questions[2].answers[0][howOld]);
        mainController.question = "What is the approximate value of your current combined retirement savings?";
        
        mainController.quizQuestion += parseInt(val) + 1;
        processSymbol(mainController.symbol);
    }
    else if (31 == mainController.quizQuestion || 32 == mainController.quizQuestion){
        mainController.answers = Object.keys(questions[3].answers[0]);
        mainController.question = questions[3].question;
        mainController.totalScore += parseInt(val) + -2 * (mainController.quizQuestion - 32);
        mainController.quizQuestion = 40;
        
        processSymbol(mainController.symbol);
    }
    else if (40 == mainController.quizQuestion){
        mainController.answers = Object.keys(questions[4].answers[0]);
        mainController.question = questions[4].question;
        
        mainController.quizQuestion += 10;
        mainController.totalScore += parseInt(val);
        mainController.image = "images/compareGraphs.png"
        processSymbol(mainController.symbol);
    }
    else if (50 == mainController.quizQuestion){
        mainController.answers = Object.keys(questions[5].answers[0]);
        mainController.question = questions[5].question;
        
        mainController.quizQuestion += 10;
        mainController.totalScore += parseInt(val);
        mainController.image = "";
        processSymbol(mainController.symbol);
    }
    else if (100 <= mainController.quizQuestion){
        if (mainController.totalScore < 13){
            //Conservative Investors: Coca-Cola(KO), H&RBlock(HRB),Lockheed Martin(LMT)
            mainController.question = "Conservative Investor";
            mainController.answers = ['Coca-Cola(KO)', 'H&RBlock(HRB)','Lockheed Martin(LMT)'];
            
            if (parseInt(val) == 0){
                mainController.symbol = 'KO';
                processSymbol(mainController.symbol);
            }
            else if (parseInt(val) == 1){
                mainController.symbol = 'HRB';
                processSymbol(mainController.symbol);
            }
            else {
                mainController.symbol = 'LMT';
                processSymbol(mainController.symbol);
            }
        }
        else if (mainController.totalScore < 27){
            //Moderate Investors: Snapchat(SNAP), Time Warner(TWX),Nike(NKE)
            mainController.question = "Moderate Investor";
            mainController.answers = ['Apolo Gold &amp; Energy(APLL)', 'Time Warner(TWX)','Nike(NKE)'];
            
            if (parseInt(val) == 0){
                mainController.symbol = 'APLL';
                processSymbol(mainController.symbol);
            }
            else if (parseInt(val) == 1){
                mainController.symbol = 'TWX';
                processSymbol(mainController.symbol);
            }
            else {
                mainController.symbol = 'NKE';
                processSymbol(mainController.symbol);
            }
        }
        else {
            //Risky Investors: Fitbit (FIT), athenahealth(ATHN), Illumina(ILMN)
            mainController.question = "Risky Investor";
            mainController.answers = ['Fitbit (FIT)', 'athenahealth(ATHN)','Illumina(ILMN)'];
            
            console.log("0");
            
            if (parseInt(val) == 0){
                mainController.symbol = 'FIT';
                processSymbol(mainController.symbol);
                console.log("1");
            }
            else if (parseInt(val) == 1){
                mainController.symbol = 'ATHN';
                processSymbol(mainController.symbol);
                console.log("2");
            }
            else {
                mainController.symbol = 'ILMN';
                processSymbol(mainController.symbol);
                console.log("3");
            }
        }
            
    }
    else {
        
        //Object.keys(questions[0].answers
        processSymbol(mainController.symbol);
        mainController.answers = Object.keys(questions[mainController.quizQuestion/10].answers[0]);
        mainController.question = questions[mainController.quizQuestion/10].question;
        
        mainController.quizQuestion += 10;
        mainController.totalScore += parseInt(val);
        
        
    }
};

module.exports = router;
