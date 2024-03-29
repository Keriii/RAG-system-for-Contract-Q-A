import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const CreatePost = () => {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        objective: "",
        file: null,
    });

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState("");
    const [accuracy, setAccuracy] = useState(null);

    const handleChange = (e) => {
        const { name, value, files } = e.target;
        setForm({ ...form, [name]: files ? files[0] : value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Create an object with the desired structure
        const data = {
            objective: form.objective // Assuming form.objective is the value you want to send
        };
    
        try {
            const response = await fetch("http://127.0.0.1:8000/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json" // Specify content type as JSON
                },
                body: JSON.stringify(data) // Stringify the object and send as the body
            });
            
            if (response.ok) {
                const responseData = await response.json();
                setResult(responseData.result);
                setAccuracy(responseData.score);
            } else {
                console.log("Failed to get a successful response from the server");
            }
        } catch (err) {
            console.error(err);
        }
    };
    
    
    return (
        <section className="bg-hero min-h-[calc(100vh)]">
            <div className="max-w-7xl bg-hero sm:p-8 px-4 mt-16 m-auto">
                <div>
                    <h1 className="font-extrabold text-text text-[42px]">Lizzy Contract Advisor</h1>
                </div>

                <form className="mt-2 form" onSubmit={handleSubmit}>
                    <div className="flex my-auto flex-col gap-5">
                        <div className="mt-2 flex flex-col">
                            <input
                                type="text"
                                name="objective"
                                placeholder="Enter Your Query"
                                value={form.objective}
                                onChange={handleChange}
                                className="border border-accent rounded-md py-2 px-3"
                            />
                            <input
                                type="file"
                                accept=".docx"
                                name="file"
                                onChange={handleChange}
                                className="mt-2 border border-accent rounded-md py-2 px-3"
                            />
                            <button
                                type="submit"
                                className="text-black bg-accent font-bold rounded-md text-sm w-full sm:w-auto px-5 py-2.5 text-center"
                            >
                                Submit
                            </button>
                        </div>
                    </div>
                    
                    <div className="relative form_photo md:m-auto border bg-darkgrey border-darkgrey text-whtie text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-64 p-3 h-64 flex flex-col items-center justify-center">
                        <div className="text-white text-center">
                            <p className="mb-2">{result ? result : "Ask me anything about the contract"}</p>
                            {accuracy && <p className="text-white mt-2">Score: {accuracy}</p>}
                        </div>
                    </div>
                </form>
            </div>
        </section>
    );
};

export default CreatePost;
