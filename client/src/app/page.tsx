import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center flex-col justify-between font-mono text-sm lg:flex">
        <h1 className="text-black">Welcome Investor</h1>
        <p>What is your investment strategy?</p>
        <p>What market are you interested in investing in?</p>
        
      </div>
    </main>
  );
}
