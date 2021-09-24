$(document).ready(function () {
    $.ajax({
        url: "/",
        type: "GET"
    })
})

$(function () {
    $("#predict_button").click(function () {
        input_data = {
            "text": $("#text").val()
        }
        console.log("xxxxxxx", input_data["text"])
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
                                window.location.href = "http://127.0.0.1:5000/";
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
