use tungstenite::connect;
use tungstenite::protocol::Message;
use url::Url;

static BINANCE_WS_API: &str = "wss://stream.binance.com:9443";
fn main() {
    // binance URL string formatter
    // TODO: make this flexible for different streams
    // example: rather than connecting to one url, create a framework for subscribing/unsubscribing to streams as we need them
    // and handling each stream uniquely
    let binance_url = format!("{}/ws/dogeusdt@bookTicker", BINANCE_WS_API);

    // connects to the websocket
    let (mut socket, response) =
        connect(Url::parse(&binance_url).unwrap()).expect("Can't connect.");

    // debug messages for initial connection to websocket
    println!("Connected to binance stream.");
    println!("HTTP status code: {}", response.status());
    println!("Response headers:");

    // print all the response headers that we get
    for (ref header, header_value) in response.headers() {
        println!("- {}: {:?}", header, header_value);
    }

    // loop that reads from the websocket
    loop {
        let msg = socket.read_message().expect("error reading message");
        // match is basically a switch
        let msg = match msg {
            // if it matches to text
            tungstenite::Message::Text(s) => s,
            // if it doesn't match to text
            _ => {
                panic!("Error getting text");
            }
        };
        // print the message
        println!("{}", msg);
    }
}
