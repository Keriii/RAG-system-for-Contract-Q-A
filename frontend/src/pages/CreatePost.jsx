import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { preview } from "../assets";
import { getRandomPrompt } from "../utils";
import { FormFields, Loader } from "../components";

const CreatePost = () => {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        objective: "",
        output: "",
        scenario: "",
    });

    const [generatingprompt, setGeneratingprompt] = useState(false);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(""); // Add this line
    const [accuracy, setAccuracy] = useState(null); // Add this line

    const handleChange = (e) =>
        setForm({ ...form, [e.target.name]: e.target.value });

    const handleSurpriseMe = () => {
        const randomPrompt = getRandomPrompt(form.scenario);
        setForm({ ...form, scenario: randomPrompt });
    };

    const generatePrompt = async () => {
        if (form.scenario) {
            try {
                setGeneratingprompt(true);
                const response = await fetch("http://192.168.137.236:8000/generate", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        num_test_output: "8",
                        objective: form.objective,
                        output: form.output,
                    }),
                });
    
                const data = await response.json();
                setResult(data.prompt);
                setAccuracy(data.score);
            } catch (err) {
                console.log(err);
            } finally {
                setGeneratingprompt(false);
            }
        } else {
            alert("Please provide a proper prompt");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        if (form.scenario && form.preview) {
            setLoading(true);
            try {
                const response = await fetch(
                    "http://192.168.137.236:8000/generate",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ ...form}),
                    }
                );
    
                if (response.ok) {
                    const responseData = await response.json();
                    const result = responseData.result;
                    console.log(result);
                } else {
                    console.log("Failed to get a successful response from the server");
                }
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        } else {
            alert("Please generate a prompt with proper details");
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
                        <FormFields
                            labelName="Query"
                            type="text"
                            name="objective"
                            placeholder="Enter Your Query"
                            value={form.objective}
                            handleChange={handleChange}
                        />
                        <input
                            type="file"
                            accept=".docx"
                            onChange={(e) => setForm({ ...form, file: e.target.files[0] })}
                        />
                        <div className="mt-2 flex flex-col">
                            <button
                                type="button"
                                onClick={generatePrompt}
                                className="text-black bg-accent font-bold rounded-md text-sm w-full sm:w-auto px-5 py-2.5 text-center"
                            >
                                {generatingprompt ? "Generating..." : "Enter"}
                            </button>
                        </div>
                    </div>
                    
                    <div className="relative form_photo md:m-auto border bg-darkgrey border-darkgrey text-whtie text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-64 p-3 h-64 flex flex-col items-center justify-center">
                        {form.preview ? (
                            <span className="text-white mb-2">
                                {result ? result : (form.results || "Ask me anything about the contract")}
                            </span>
                        ) : (
                            <div className="text-white text-center">
                                <p className="mb-2">{result ? result : (form.results || "Ask me anything about the contract")}</p>
                                {accuracy && <p className="text-white mt-2">Score: {accuracy}</p>}
                            </div>
                        )}
                    </div>
                </form>
            </div>
        </section>
    );
};

export default CreatePost;
