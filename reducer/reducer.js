var http = require('http');
var url = require('url');

const PORT = process.env.PORT || 8003;

http.createServer(function (request, response) {
    if(request.method === 'POST') {
 
        var data = '';
    
        request.on('data', function(chunk) {data += chunk})
               .on('end', function() {
 
            console.log("Received: ", data);
            var dict_list = JSON.parse(data);
//          console.log(JSON.stringify(dict_list));

            reduced = {}
            for (const dict of dict_list) {
                var key = Object.keys(dict)[0]
                console.log("DEBUG : ", key);
                if (key in reduced) {
                    reduced[key] += 1;
                }
                else {
                    reduced[key] = 1;
                }
            }
            console.log("Response: ", reduced);

            response.writeHead(200, {'Content-Type' : 'application/json'});
            response.end(JSON.stringify(reduced));
 
          })
 
    }
}).listen(PORT);

console.log(`Server is listening on port ${PORT}`);
