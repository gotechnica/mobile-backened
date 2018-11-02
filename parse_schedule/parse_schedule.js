var fs = require('fs');
var moment = require('moment');

let scheduleFile = process.argv[2];
//console.log(scheduleFile);

// maps first name to id
let satObj = [];
let sunObj = [];

let dayMap = {"Saturday" : satObj, "Sunday" : sunObj};

finalJson = {"Schedule" : [["Saturday", satObj], ["Sunday", sunObj]], "Updates" : {}};

fs.readFile(scheduleFile, 'utf8', (err, data) => {

 if(err){
   throw err;
 } else {

   //console.log(data);
   data = data.replace(/"/g, "");
   let lines = data.split("\r\n");

   for(let i = 1; i < lines.length; i++){
     let line = lines[i];
     // split column by comma
     fields = line.split(",")
     eventObj = {
         "beginnerFriendly" : (fields[14] == "Yes" ? true : false),
         "description" : fields[13],
         "endTime" : moment(fields[11], "M/D/YYYY HH:mm:ss").format("YYYY-MM-DD HH:mm"),
         "eventID" : (100000 + i).toString(),
         "img" : fields[15],
         "location" : fields[12],
         "startTime" : moment(fields[6], "M/D/YYYY HH:mm:ss").format("YYYY-MM-DD HH:mm"),
         "title" : fields[1]
       };
       //console.log(eventObj)
       //console.log(fields[0]);
     dayMap[fields[0]].push(JSON.stringify(eventObj));
   }

   out = JSON.stringify(finalJson, null, 4);
   out = out.replace(/"{/g, "{");
   out = out.replace(/}"/g, "}");
   out = out.replace(/\\\"/g, "\""); // replace \" with just "
   out = out.replace(/\\\\n/g, "\\n"); // replace \\n with \n
   out = out.replace(/-_-/g, ","); // replace -_- with , (to avoid conflict with comma separated columns)
   out = out.replace(/,"/g, ",\n\"")
   fs.writeFileSync('scheduleOutput.json', out);
 }
});