extern crate ethabi;

// use ethabi::{encode, decode, ParamType, Token};   
// mod signing_types;
use std::any::Any;
mod signing_types;
use signing_types::{Tif, Tpsl, LimitOrderType, TriggerOrderType, TriggerOrderTypeWire, OrderType,
OrderTypeWire, OrderRequest, CancelRequest};

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
#[derive(Debug, PartialEq)]
enum Grouping {
    Na,
    NormalTpsl,
    PositionTpsl,
}

fn order_grouping_to_number(grouping: Grouping) -> i32 {
    match grouping {
        Grouping::Na => 0,
        Grouping::NormalTpsl => 1,
        Grouping::PositionTpsl => 2,
    }
}

#[derive(Debug, PartialEq)]
struct Order {
    asset: i32,
    is_buy: bool,
    limit_px: f64,
    sz: f64,
    reduce_only: bool,
}

#[derive(Debug, PartialEq)]
struct OrderSpec {
    order: Order,
    order_type: OrderType,
}

#[derive(Debug, PartialEq)]
struct Order {
    asset: i32,
    is_buy: bool,
    limit_px: f64,
    sz: f64,
    reduce_only: bool,
}

fn order_spec_preprocessing(order_spec: &OrderSpec) -> Result<(i32, bool, i32, i32, bool, i32, i32), &'static str> {
    let order = &order_spec.order;
    let order_type_array = order_type_to_tuple(&order_spec.order_type)?;
    
    let asset = order.asset;
    let is_buy = order.is_buy;
    let limit_px = float_to_int_for_hashing(order.limit_px);
    let sz = float_to_int_for_hashing(order.sz);
    let reduce_only = order.reduce_only;
    let order_type_code = order_type_array.0;
    let order_type_value = float_to_int_for_hashing(order_type_array.1);

    Ok((asset, is_buy, limit_px, sz, reduce_only, order_type_code, order_type_value))
}

#[derive(Debug, PartialEq)]
struct OrderWire {
    asset: i32,
    is_buy: bool,
    limit_px: String,
    sz: String,
    reduce_only: bool,
    order_type: OrderTypeWire,
}

fn order_type_to_wire(order_type: &OrderType) -> Result<OrderTypeWire, &'static str> {
    match order_type {
        OrderType::Limit => Ok(OrderTypeWire { limit: order_type.limit.clone() }), // Assuming you have a clone method for OrderTypeWire
        OrderType::Trigger { trigger_px, tpsl, is_market } => Ok(OrderTypeWire {
            trigger: TriggerOrderTypeWire {
                trigger_px: float_to_wire(*trigger_px)?,
                tpsl: tpsl.clone(),
                is_market: *is_market,
            },
        }),
    }
}



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
