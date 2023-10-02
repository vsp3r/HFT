extern crate ethabi;

// use ethabi::{encode, decode, ParamType, Token};
mod signing;

fn main() {
    // Define an Ethereum function signature.
    signing::signing_fn();
    
}
