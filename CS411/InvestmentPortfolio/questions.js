
var questions = [
    {
        "question": "What is your current age?",
        "answers": [{
            "Over 60" : "0",
            "50-59" : "1",
            "40-49" : "2",
            "30-39" : "3",
            "Under 29" : "4"
        }]
    }
    ,{
        "question": "How would you rate your current level of investment knowledge/understanding?",
        "answers":[{
            "Poor":"0",
            "Limited":"1",
            "Average":"2",
            "Good":"3",
            "Excellent":"4"
        }]
    }
    ,{
        "question": "How old are you?",
        "answers":[
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
        ]
    }
    ,{
        "question": "How many years until you begin to take money from your retirement savings?",
        "answers":[
            {
                "0-5":"0",
                "5-10":"1",
                "11-20":"2",
                "21-30":"3",
                "31-40+":"4"
            }
        ]
    }
    ,{
        "question": "Below is a hypothetical growth of a $10,000 investment for three accounts over the next nine years. Which portfolio would you prefer",
        "answers":[
            {
                "Portfolio 1":"0",
                "Portfolio 2":"2",
                "Portfolio 3":"4",
            }
        ],
        "image":"img/url"
    }
    ,{
        "question": "Rank this statement: My retirement income will be satisfactory with only my 401(K)?",
        "answers":[
            {
                "Strongly Agree":"0",
                "Agree":"1",
                "Neutral":"2",
                "Disagree":"3",
                "Strongly Disagree":"4"
            }
        ]
    }
    ,{
        "question": "What stage are you in your life?",
        "answers":[
            {
                "Retired":"0",
                "Semi-Retired":"1",
                "Late Stage Career":"2",
                "Early Mid Stage Career":"3",
                "Beginning Career":"4"
            }
        ]
    }
    ,{
        "question": "What is the number of consecutive years you would be willing to accept your account performance to be flat or negative?",
        "answers":[
            {
                "0 Years":"0",
                "1 Years":"1",
                "2 Years":"2",
                "3 Years":"3",
                "4 or More Years":"4"
            }
        ]
    }
    ,{
        "question": "Rank this statement: My retirement goals have been obtained. I wish for my account to maintain its value, with some income.",
        "answers":[
            {
                "Strongly Agree":"0",
                "Agree":"1",
                "Neutral":"2",
                "Disagree":"3",
                "Strongly Disagree":"4"
            }
        ]
    }
    ,{
        "question": "Rank this statement: I will need to make withdrawls from my account within the next five years",
        "answers":[
            {
                "Strongly Agree":"0",
                "Agree":"1",
                "Neutral":"2",
                "Disagree":"3",
                "Strongly Disagree":"4"
            }
        ]
    }
]

module.exports.questions = questions