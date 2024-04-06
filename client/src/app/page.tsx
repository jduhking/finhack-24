import { Select } from "@radix-ui/themes";
import { Lato } from "next/font/google";

export default function Home() {
  return (
    <main className={`flex min-h-screen text-black flex-col items-center justify-between p-24 `}>
      <div className={`z-10 max-w-5xl w-full items-center flex-col justify-between font-mono text-sm lg:flex`}>
        <h1 className={`text-4xl mb-10`}>Welcome Investor</h1>
          <div className='mb-10 flex flex-col'>
            <h1 className="mb-11">What is your investment strategy?</h1>
            <div>
              <Select.Root defaultValue="activist">
              <Select.Trigger />
              <Select.Content>
                  <Select.Item value="activist">Activist</Select.Item>
                  <Select.Item value="growth">Growth</Select.Item>
              </Select.Content>
              </Select.Root>
            </div>
          </div>
          <div className='mb-10 flex flex-col'>
            <h1 className="mb-11">What market are you interested in investing in?</h1>
            <div>
              <Select.Root defaultValue="tech">
              <Select.Trigger />
              <Select.Content>
                  <Select.Item value="tech">Tech</Select.Item>
                  <Select.Item value="gas">Gas</Select.Item>
                  <Select.Item value="health">Health</Select.Item>
              </Select.Content>
              </Select.Root>
            </div>
          </div>
        </div>
    </main>
  );
}
