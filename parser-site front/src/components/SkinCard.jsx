import { Card } from 'antd';

function SkinCard(props) {

  const { item, type } = props
  return (
    <>
      <Card title={item.name} style={{ width: 300 }}>
        { props.type === "m9" ? (
          <div className="flex">
          <div className="mr-4">
            <p>steam fn {item.steam_fn}</p>
            <p>steam mw {item.steam_mw}</p>
            <p>steam ww {item.steam_ww}</p>
            <p>steam ft {item.steam_ft}</p>
            <p>steam bs {item.steam_bs}</p>
          </div>
          <div>
            <p>buff fn {item.buff_fn}</p>
            <p>buff mw {item.buff_mw}</p>
            <p>buff ww {item.buff_ww}</p>
            <p>buff ft {item.buff_ft}</p>
            <p>buff bs {item.buff_bs}</p>
          </div>
        </div>
        ) : props.type === "case" ? (
          <div>
            <p>buff buy {item.buff_buy}</p>
            <p>buff sell {item.buff_sell}</p>
            <p>steam sell {item.steam_sell}</p>
          </div>
        ) : (
          <p>no item</p>
        )}
      </Card>
    </>
  )
}
  
  export default SkinCard