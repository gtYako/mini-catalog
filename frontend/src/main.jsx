import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import Catalog from './pages/Catalog'
import Service from './pages/Service'
import Request from './pages/Request'
import Manage from './pages/Manage'
import './style.css'
function App(){
 const [favorites,setFavorites]=useState(()=>{try{return JSON.parse(localStorage.getItem('favorites') || '[]')}catch{return []}})
 function toggle(id){setFavorites(old=>{const next=old.includes(id)?old.filter(x=>x!==id):[...old,id];localStorage.setItem('favorites',JSON.stringify(next));return next})}
 return <><header><nav><Link to="/">Каталог</Link><Link to="/request">Оставить заявку</Link><Link to="/manage">Управление</Link></nav></header><main><Routes><Route path="/" element={<Catalog favorites={favorites} toggle={toggle}/>}/><Route path="/services/:id" element={<Service/>}/><Route path="/request" element={<Request/>}/><Route path="/manage" element={<Manage/>}/><Route path="*" element={<p>Страница не найдена. <Link to="/">В каталог</Link></p>}/></Routes></main></>
}
createRoot(document.getElementById('root')).render(<BrowserRouter><App/></BrowserRouter>)
