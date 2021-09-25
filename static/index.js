// Using an offset to calculate Timezone is a wrong approach, and you will always encounter problems. 
// Time zones and daylight saving rules may change on several occasions during a year &
// It's difficult to keep up with changes!!

// TIMEZONE OFFSET
// var date = new Date()
// var tz_offset_mins = date.getTimezoneOffset();
// console.log(tz_offset_mins)

//GET System's IANA timezone
local_timezone = Intl.DateTimeFormat().resolvedOptions().timeZone
var date = new Date()
const weekDay = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
const month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

display_date = `${weekDay[date.getDay()-1]}, ${date.getDate()} ${month[date.getMonth()]} ${date.getFullYear()}`

$(document).ready(function () {  
    timezone_data = {"timezone":local_timezone, "date":display_date}   
    console.log(timezone_data)
    $.ajax({       
        url: "/",
        type: "GET",
        success: function(){
            $("#display_date").html(display_date)
        }
    })
})

$(function () {
    $("#predict_button").click(function () {
        input_data = {
            "text": $("#text").val()
        }        
        if (input_data["text"] == "") {
            alert("Please enter some text to predict emotion!!")
        }
        else {
            $.ajax({
                type: 'POST',
                url: "/predict-emotion",
                data: JSON.stringify(input_data),
                dataType: "json",
                contentType: 'application/json',
                success: function (prediction_result) {

                    $("#prediction").html(prediction_result[0])
                    $("#emo_img_url").attr('src', prediction_result[1]);
                    $('#prediction').css("display", "");
                    $('#emo_img_url').css("display", "");

                    $("#save_button").click(function () {
                        save_data={
                            "date":display_date,
                            "text":input_data["text"],
                            "emotion":prediction_result[0]
                        }
                        $.ajax({
                            type: 'POST',
                            url: "/save-entry",
                            data: JSON.stringify(save_data),
                            dataType: "json",
                            contentType: 'application/json',
                            success: function () {                                
                                alert("Your entry has been saved successfully!!")
                            },
                            complete: function(){
                                window.location.href = "https://digital-diary-web-app.herokuapp.com/";
                            },
                            error: function (result) {
                                alert(result.responseJSON.message)
                            }
                        });
                        
                    });

                },
                error: function (result) {
                    alert(result.responseJSON.message)
                }
            });
        }
    });
})
