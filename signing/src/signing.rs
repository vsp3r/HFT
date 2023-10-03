extern crate ethabi;

// use ethabi::{encode, decode, ParamType, Token};   
// mod signing_types;
use std::any::Any;
mod signing_types;
use signing_types::{Tif, Tpsl, LimitOrderType, TriggerOrderType, TriggerOrderTypeWire, OrderType,
OrderTypeWire, OrderRequest, CancelRequest, Grouping, Order, OrderSpec, OrderWire};

fn order_type_to_tuple(order_type: &OrderType) -> Result<(i32, f64), &'static str> {
    match order_type {
        OrderType::Limit { tif } => match tif {
            Tif::Gtc => Ok((2, 0.0)),
            Tif::Alo => Ok((1, 0.0)),
            Tif::Ioc => Ok((3, 0.0)),
        },
        OrderType::Trigger {
            trigger_px,
            is_market,
            tpsl,
        } => match (is_market, tpsl) {
            (true, Tpsl::Tp) => Ok((4, *trigger_px)),
            (false, Tpsl::Tp) => Ok((5, *trigger_px)),
            (true, Tpsl::Sl) => Ok((6, *trigger_px)),
            (false, Tpsl::Sl) => Ok((7, *trigger_px)),
        },
    }
}

fn order_type_to_tuple(order_type: &OrderType) -> (i32, f64){
    match order_type {
        OrderType::Limit => match tif
    }
}

fn order_grouping_to_number(grouping: Grouping) -> i32 {
    match grouping {
        Grouping::Na => 0,
        Grouping::NormalTpsl => 1,
        Grouping::PositionTpsl => 2,
    }
}



// fn order_spec_preprocessing(order_spec: &OrderSpec) -> Result<(i32, bool, i32, i32, bool, i32, i32), &'static str> {
//     let order = &order_spec.order;
//     let order_type_array = order_type_to_tuple(&order_spec.order_type)?;
    
//     let asset = order.asset;
//     let is_buy = order.is_buy;
//     let limit_px = float_to_int_for_hashing(order.limit_px);
//     let sz = float_to_int_for_hashing(order.sz);
//     let reduce_only = order.reduce_only;
//     let order_type_code = order_type_array.0;
//     let order_type_value = float_to_int_for_hashing(order_type_array.1);

//     Ok((asset, is_buy, limit_px, sz, reduce_only, order_type_code, order_type_value))
// }



// fn order_type_to_wire(order_type: &OrderType) -> Result<OrderTypeWire, &'static str> {
//     match order_type {
//         OrderType::Limit => Ok(OrderTypeWire { limit: order_type.limit.clone() }), // Assuming you have a clone method for OrderTypeWire
//         OrderType::Trigger { trigger_px, tpsl, is_market } => Ok(OrderTypeWire {
//             trigger: TriggerOrderTypeWire {
//                 trigger_px: float_to_wire(*trigger_px)?,
//                 tpsl: tpsl.clone(),
//                 is_market: *is_market,
//             },
//         }),
//     }
// }



fn main() {
    // Example usage:
    let limit_order = LimitOrderType { tif: Tif::Alo };
    let tpsl_order = TriggerOrderType {
        trigger_px: 42.0,
        is_market: true,
        tpsl: Tpsl::Tp,
    };
    let order_type = OrderType {
        limit: limit_order,
        trigger: tpsl_order,
    };
    let order_request = OrderRequest {
        coin: "BTC".to_string(),
        is_buy: true,
        sz: 1.0,
        limit_px: 50000.0,
        order_type,
        reduce_only: false,
    };
    
    println!("{:#?}", order_request);
}


// sends bulk orders
// list of order specs (asset, isbuy, reduceonly, limipx, sz), and ordertype
// signature = sign_l1(wallet, sig_types, sig_data, active_pool, nonce, is_mainnet?)
// signature = sign_l1_action(
//     self.wallet,
//     ["(uint32,bool,uint64,uint64,bool,uint8,uint64)[]", "uint8"],
//     [[order_spec_preprocessing(order_spec) for order_spec in order_specs], order_grouping_to_number(grouping)],
//     ZERO_ADDRESS if self.vault_address is None else self.vault_address,
//     timestamp,
//     self.base_url == MAINNET_API_URL,
// )

// sig_types seems self explanatory
// sig_data needs order_spec prepreocessing


// order_spec_preprocessing
// taks in order_spec of type OrderSpec (order, orderType)
// ordertype = limit or trigger
// 
