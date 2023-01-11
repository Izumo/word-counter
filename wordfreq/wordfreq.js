var http = require('http');
var url = require('url');

var hostname = '127.0.0.1';
const PORT = process.env.PORT || 8000;

http.createServer(function (request, response) {
    if(request.method === 'POST') {
 
        var data = '';
    
        request.on('data', function(chunk) {data += chunk})
               .on('end', function() {
 
            console.log("Received: ", data);
//          console.log(JSON.stringify(request_data));
            var lines = data.split('\n');

            console.log(JSON.stringify(lines));

            response.writeHead(200, {'Content-Type' : 'text/json'});
            response.end("done"); //JSON.stringify(word_dicts));
 
          })
 
    }
}).listen(PORT);

console.log(`Server is listening on port ${PORT}`);
