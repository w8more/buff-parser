import React, { useEffect, useState } from 'react';
// import { AppstoreOutlined, MailOutlined, SettingOutlined } from '@ant-design/icons';
import { Menu, Spin } from 'antd';
import axios from 'axios';
import SkinCard from "./components/SkinCard.jsx";

function getItem(label, key, icon, children, type) {
  return {
    key,
    icon,
    children,
    label,
    type,
  };
}

const App = () => {
  const [itemtypes, setItemTypes] = useState([])
  const [items, setItems] = useState([])
  const [selectedItemType, selectItemType] = useState("case")
  const [selectedItem, selectItem] = useState(0)
  const [itemData, setItemData] = useState(null)

  const fetchItemTypes = () => {
    axios.get("http://127.0.0.1:8000/item/get_all_item_types").then(r => {
      const itemTypesResponse = r.data
      const menuItemTypes = [
        getItem('Item type list', 'g1', null, itemTypesResponse.map(i =>{
          return {label: i, key: i}
        }), 
        'group'),
      ]
      setItemTypes(menuItemTypes)
    })
  }

  const fetchItems = (item_type) => {
    axios.get(`http://127.0.0.1:8000/item/get_items/${item_type}`).then(r => {
      console.log(`selectedItemType = ${selectedItemType}`);
      const itemsResponse = JSON.parse(r.data)
      const itemList = Object.entries(itemsResponse.name).map(([key, name]) => ({
        label: name,
        key
      }));

      const menuItems = [
        getItem('Item list', 'g1', null, itemList, 'group')
      ];

      setItems(menuItems)
    })
  }

  const fetchItem = () => {
    axios.get(`http://127.0.0.1:8000/item/get_item/${selectedItemType}/${selectedItem}`).then(r => {
      const itemsResponse = JSON.parse(r.data)
      setItemData(itemsResponse)
    })
  }

  useEffect( () => {
    fetchItemTypes();
    fetchItems(selectedItemType);
  }, []);

  useEffect( () => {
    setItemData(null)
    fetchItem()
  }, [selectedItem]); 

  const handleItemClick = (item_type) => {
    if (selectedItemType !== item_type.key) {
      selectItemType(item_type.key);
      fetchItems(item_type.key);
    }
  };

  const handleItemSelect = (item) => {
    selectItem(item.key)
  };

  return (
    <div className="flex">
      <Menu
        onClick={handleItemSelect}
        style={{
          width: 256,
        }}
        defaultSelectedKeys={['1']}
        defaultOpenKeys={['sub1']}
        mode="inline"
        items={items}
        className="h-screen overflow-scroll items-center"
      />
    
      <div className="w-full flex justify-center">
        <Menu
          onClick={handleItemClick}
          style={{
            width: 256,
          }}
          defaultSelectedKeys={['1']}
          defaultOpenKeys={['sub1']}
          mode="horizontal"
          items={itemtypes}
          className="flex"
        />
      </div>
      <div className="mx-auto my-auto">
        {itemData ? <SkinCard item={itemData} type={selectedItemType}/> : <Spin size="large"/>}
      </div>
    </div>

  );
};
export default App;