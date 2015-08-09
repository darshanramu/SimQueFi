function requestAll(urll, callback, req) {
    
    
   
    $.ajax({
        url: urll,
        // this is the parameter list
        data: "",
        type: 'GET',
        success: function (output) {
            // parse the data here
            try {
                //output = JSON.parse(output);
            }
            catch (err) {
                output = {
                    "error": "JSON parse error",
                    "errorccode": "1"
                }
            }
            callback(output);
        },
        error: function (msg) {
            console.log(msg);
        }
    });

}
function reset(){
    $("#results")[0].innerHTML="";
}
function clicked(oObj){
var tags=$("#tags").val();
    var titles=$("#title").val();
    
    var urll="https://api.stackexchange.com/2.2/search?order=desc&sort=creation&site=stackoverflow";
    if(tags.length>0){
        urll+="&tagged="+tags;
    }
    if(titles.length>0){
        urll+="&intitle="+titles;
    }
    requestAll(urll,logToCon);
}

function logToCon(output){
    var res=$("#results");
     var de;
    for(i=0;i<output.items.length;i++){
      res.append($("<div>").text(output.items[i].title.toLowerCase()));
       
      //  res.append($("<div>").text(output.items[i].title));
    }
    
}
