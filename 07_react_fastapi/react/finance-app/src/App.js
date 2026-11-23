import { useEffect, useState } from "react";
import api from "./api";

const App = ()=> {
  const [transactions,setTransaction] = useState([]);
  const [formData,setFormData] = useState({
    amount: '',
    category: '',
    description: '',
    is_income: false,
    date: ''
  })

  const fetchTransactions = async()=>{
    const response = await api.get("/transactions/");
    setTransaction(response.data)
  };

  useEffect(()=>{
    fetchTransactions();
  },[])

}

export default App;
