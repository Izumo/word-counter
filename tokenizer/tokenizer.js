var http = require('http');
var url = require('url');

var hostname = '127.0.0.1';
const PORT = process.env.PORT || 8001;

http.createServer(function (request, response) {
    if(request.method === 'GET') {
 
        var line = url.parse(request.url, true).query.line;
        console.log("Received: ", line);
        var tokens = line.split(' ');
        console.log("Response: ", tokens);

        response.writeHead(200, {'Content-Type' : 'application/json'});
        response.end(JSON.stringify(tokens));
 
    }
}).listen(PORT);

console.log(`Server is listening on port ${PORT}`);
