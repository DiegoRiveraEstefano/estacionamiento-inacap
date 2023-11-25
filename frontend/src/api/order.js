import axios from 'axios'
const apiUrl = "http://127.0.0.1:8000/"


export default async function getPaymentLink(orderCode){
    const config = {
        url: apiUrl + "order/" + orderCode,
        method: 'get',
        headers: {},
    }
    try{
        const result = await axios.request(config)
        return result.data;
    }catch(error){
        return null
    }
}

export async function getPaymentStatus(orderCode){
    const config = {
        url: apiUrl + "order/" + orderCode + '/',
        method: 'get',
        headers: {},
    }
    try{
        const result = await axios.request(config)
        return result.data;
    }catch(error){
        return null
    }
}