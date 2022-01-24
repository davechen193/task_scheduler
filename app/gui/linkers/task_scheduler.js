const { clipboard } = require('electron')
const keyCodes = {
  V: 86,
}
document.onkeydown = function(event){
  let toReturn = true
  if(event.ctrlKey || event.metaKey){  // detect ctrl or cmd
    if(event.which == keyCodes.V){
      document.activeElement.value += clipboard.readText()
      document.activeElement.dispatchEvent(new Event('input'))
      toReturn = false
    }
  }

  return toReturn
}
function schedules(){
  input_text = document.getElementById("input").value;
  const { spawn } = require('child_process');
  const fs = require('fs');
  fs.writeFile(__dirname + '/../tasks.txt', input_text, (err) => {
    if (err) throw err;
  })
  const proc = spawn('/usr/local/bin/python3', [__dirname + '/../task_scheduler.py', __dirname + '/../tasks.txt']);
  proc.stdout.on('data', (data) => {
    document.getElementById("output").style.fontSize = "medium";
    document.getElementById("output").innerHTML= data.toString();
  });
  proc.stderr.on('data', (data) => {
    document.getElementById("output").innerHTML= data.toString();
  });
}