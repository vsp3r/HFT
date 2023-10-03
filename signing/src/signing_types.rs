#[derive(Debug)]
pub enum Tif {
    Alo,
    Ioc,
    Gtc,
}

#[derive(Debug)]
pub enum Tpsl {
    Tp,
    Sl,
}

#[derive(Debug)]
pub struct LimitOrderType {
    pub tif: Tif,
}

#[derive(Debug)]
pub struct TriggerOrderType {
    pub trigger_px: f64,
    pub is_market: bool,
    pub tpsl: Tpsl,
}

#[derive(Debug)]
pub struct TriggerOrderTypeWire {
    pub trigger_px: String,
    pub is_market: bool,
    pub tpsl: Tpsl,
}

#[derive(Debug)]
pub struct OrderType {
    pub limit: LimitOrderType,
    pub trigger: TriggerOrderType,
}
// TODO: might want to replace ordertype with an enum, so match statement can be used
#[derive(Debug)]
pub enum OrderType {
    Limit,
    Trigger
}


#[derive(Debug)]
pub struct OrderTypeWire {
    pub limit: LimitOrderType,
    pub trigger: TriggerOrderTypeWire,
}

#[derive(Debug)]
pub struct OrderRequest {
    pub coin: String,
    pub is_buy: bool,
    pub sz: f64,
    pub limit_px: f64,
    pub order_type: OrderType,
    pub reduce_only: bool,
}

#[derive(Debug)]
pub struct CancelRequest {
    pub coin: String,
    pub oid: i32,
}

#[derive(Debug)]
pub enum Grouping {
    Na,
    NormalTpsl,
    PositionTpsl,
}

#[derive(Debug)]
pub struct Order {
    pub asset: i32,
    pub is_buy: bool,
    pub limit_px: f64,
    pub sz: f64,
    pub reduce_only: bool,
}

#[derive(Debug)]
pub struct OrderSpec {
    pub order: Order,
    pub order_type: OrderType,
}

#[derive(Debug)]
pub struct OrderWire {
    pub asset: i32,
    pub is_buy: bool,
    pub limit_px: String,
    pub sz: String,
    pub reduce_only: bool,
    pub order_type: OrderTypeWire,
}