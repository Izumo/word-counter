var http = require('http');
var url = require('url');

var hostname = '127.0.0.1';
const PORT = process.env.PORT || 8002;

http.createServer(function (request, response) {
    if(request.method === 'POST') {
 
        var data = '';
    
        request.on('data', function(chunk) {data += chunk})
               .on('end', function() {
 
            console.log("Received: ", data);
            var word_list = JSON.parse(data);
//          console.log(JSON.stringify(word_list));

            var word_dicts = [];
            for (const word of word_list) {
                if (word.length > 0) {
                    var item = {};
                    item[word] = 1;
                    word_dicts.push(item);
                }
            }
            console.log("Response: ", word_dicts);

            response.writeHead(200, {'Content-Type' : 'text/json'});
            response.end(JSON.stringify(word_dicts));
 
          })
 
    }
}).listen(PORT);

console.log(`Server is listening on port ${PORT}`);
