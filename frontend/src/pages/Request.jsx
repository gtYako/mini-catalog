import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api, fieldError } from '../api/client'
export default function Request() {
  const [params] = useSearchParams(), [services, setServices] = useState([]), [data, setData] = useState({service:params.get('service') || '', client_name:'', phone:'', desired_at:''})
  const [errors, setErrors] = useState({}), [message, setMessage] = useState(''), [number, setNumber] = useState(null), [busy, setBusy] = useState(false), [retry, setRetry] = useState(0)
  useEffect(() => { let active=true; async function load() { try { let path='/services/?is_available=true', all=[]; while (path) { const r=await api(path); all=all.concat(r.results); path=r.next ? new URL(r.next).pathname.replace(/^\/api/, '') + new URL(r.next).search : null } if(active) {setServices(all); setMessage('')} } catch(e) { if(active) setMessage(e.message) } } load(); return () => {active=false} }, [retry])
  const change = e => setData({...data,[e.target.name]:e.target.value})
  async function submit(e) { e.preventDefault(); if(busy) return; setBusy(true); setErrors({}); setMessage(''); setNumber(null)
    try { const result=await api('/requests/', {method:'POST',body:JSON.stringify({...data, desired_at:data.desired_at ? new Date(data.desired_at).toISOString() : ''})}); setNumber(result.id) }
    catch(e) { setErrors(e.data || {}); setMessage(e.message) } finally {setBusy(false)} }
  return <><h1>Оставить заявку</h1><form onSubmit={submit} noValidate>
    <label>Услуга<select name="service" value={data.service} onChange={change}><option value="">Выберите услугу</option>{services.map(s=><option key={s.id} value={s.id}>{s.name}</option>)}</select><small>{fieldError(errors,'service')}</small></label>
    <label>Ваше имя<input name="client_name" value={data.client_name} onChange={change}/><small>{fieldError(errors,'client_name')}</small></label>
    <label>Телефон<input name="phone" value={data.phone} onChange={change}/><small>{fieldError(errors,'phone')}</small></label>
    <label>Дата и время<input type="datetime-local" name="desired_at" value={data.desired_at} onChange={change}/><small>{fieldError(errors,'desired_at')}</small></label>
    {message && <p className="error" role="alert">{message} <button type="button" onClick={()=>setRetry(retry+1)}>Повторить загрузку услуг</button></p>}
    {number && <p className="success">Заявка создана. Номер: {number}</p>}
    <button disabled={busy}>{busy ? 'Отправка...' : 'Отправить'}</button>
  </form></>
}
