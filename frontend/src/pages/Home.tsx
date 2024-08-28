import { FormEvent, useState } from "react";
import api from "../api";

export default function Home() {
    const [loading, setLoading] = useState<boolean>(false);

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        setLoading(true);
        e.preventDefault();
        const nip = 6751441570;

        try {
            const res = await api.get(`/api/nip/${nip}/`, {
                headers: {
                    Authorization: `Token 77037f3dbde9931cb2590e740e1ba985e5dc7dbe`,
                },
            });

            console.log(JSON.parse(res.data))

        } catch (error) {
            console.log(error)
        } finally {
            setLoading(false)
        }
    };


    return <form onSubmit={(e) => handleSubmit(e)}>
        <button type="submit">
            GET
        </button>
        {loading}
    </form>
}