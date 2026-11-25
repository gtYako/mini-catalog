import { useCallback, useEffect, useState } from 'react'
import { api, fieldError } from '../api/client'
const blank = {name:'', description:'', category:'', price:'', duration_minutes:'', is_available:true}
export default function Manage() {
  const [staff,setStaff]=useState(false), [auth,setAuth]=useState({username:'',password:''}), [items,setItems]=useState([]), [categories,setCategories]=useState([])
  const [form,setForm]=useState(blank), [editing,setEditing]=useState(null), [errors,setErrors]=useState({}), [message,setMessage]=useState(''), [success,setSuccess]=useState(''), [busy,setBusy]=useState(false), [loading,setLoading]=useState(true)
  const refresh=useCallback(async()=>{setLoading(true); try {const info=await api('/session/'); setStaff(info.is_staff); if(info.is_staff) { let all=[], path='/services/'; while(path){const r=await api(path); all=all.concat(r.results); path=r.next ? new URL(r.next).pathname.replace(/^\/api/,'')+new URL(r.next).search : null} setItems(all); const cats=await api('/categories/'); setCategories(cats.results) } setMessage('')} catch(e){setMessage(e.message)} finally{setLoading(false)}},[])
  useEffect(()=>{refresh()},[refresh])
  async function login(e){e.preventDefault();setBusy(true);setMessage('');try{await api('/login/',{method:'POST',body:JSON.stringify(auth)});await refresh();setAuth({username:'',password:''})}catch(err){setMessage(err.message)}finally{setBusy(false)}}
  async function save(e){e.preventDefault(); if(busy)return;setBusy(true);setMessage('');setSuccess('');setErrors({});try{await api(editing ? '/services/'+editing+'/' : '/services/',{method:editing?'PATCH':'POST',body:JSON.stringify(form)});setForm(blank);setEditing(null);await refresh();setSuccess('Услуга сохранена')}catch(err){setErrors(err.data || {});setMessage(err.message)}finally{setBusy(false)}}
  async function remove(id){if(!window.confirm('Удалить эту услугу?'))return;setBusy(true);setMessage('');setSuccess('');try{await api('/services/'+id+'/',{method:'DELETE'});await refresh();setSuccess('Услуга удалена')}catch(err){setMessage(err.message)}finally{setBusy(false)}}
  async function signout(){try{await api('/logout/',{method:'POST'});setStaff(false);setItems([]);setSuccess('')}catch(err){setMessage(err.message)}}
  if(loading)return <p>Загрузка...</p>
  return <><h1>Управление каталогом</h1>{message && <p className="error" role="alert">{message} <button onClick={refresh}>Повторить</button></p>}{success && <p className="success">{success}</p>}
    {!staff ? <form onSubmit={login}><p>Войдите под администратором Django.</p><label>Логин<input value={auth.username} onChange={e=>setAuth({...auth,username:e.target.value})}/></label><label>Пароль<input type="password" value={auth.password} onChange={e=>setAuth({...auth,password:e.target.value})}/></label><button disabled={busy}>Войти</button></form> : <>
      <button onClick={signout}>Выйти</button><h2>{editing ? 'Редактирование услуги' : 'Добавить услугу'}</h2>
      <form onSubmit={save} noValidate>
      {['name','description','price','duration_minutes'].map(key=><label key={key}>{{name:'Название',description:'Описание',price:'Цена',duration_minutes:'Длительность в минутах'}[key]}<input type={['price','duration_minutes'].includes(key)?'number':'text'} name={key} value={form[key]} onChange={e=>setForm({...form,[key]:e.target.value})}/><small>{fieldError(errors,key)}</small></label>)}
      <label>Категория<select value={form.category} onChange={e=>setForm({...form,category:e.target.value})}><option value="">Выберите категорию</option>{categories.map(c=><option value={c.id} key={c.id}>{c.name}</option>)}</select><small>{fieldError(errors,'category')}</small></label>
      <label className="check"><input type="checkbox" checked={form.is_available} onChange={e=>setForm({...form,is_available:e.target.checked})}/> Доступна</label>
      <div className="actions"><button disabled={busy}>Сохранить</button>{editing && <button type="button" onClick={()=>{setEditing(null);setForm(blank);setErrors({})}}>Отмена</button>}</div></form>
      <h2>Все услуги</h2>{!items.length && <p>Услуг пока нет.</p>}<div className="cards">{items.map(s=><article className="card" key={s.id}><strong>{s.name}</strong><p>{s.category_name} · {s.price} ₽ · {s.is_available?'доступна':'недоступна'}</p><div className="actions"><button onClick={()=>{setEditing(s.id);setForm({name:s.name,description:s.description,price:s.price,duration_minutes:s.duration_minutes,category:s.category,is_available:s.is_available});setSuccess('');setErrors({});window.scrollTo(0,0)}}>Изменить</button><button disabled={busy} onClick={()=>remove(s.id)}>Удалить</button></div></article>)}</div>
    </>}</>
}
