export default function Intro() {
  return (
    <>
      <div className="pt-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl leading-9 font-extrabold sm:text-4xl sm:leading-10">
            Introducing Atlus: Your Ultimate Address Parsing Solution!
          </h2>
          <p className="mt-3 text-xl leading-7 sm:mt-4">
            Struggling to accurately tag addresses for your mapping projects?
            Look no further! Atlus is your all-in-one solution for effortlessly
            parsing raw address strings into OpenStreetMap-compatible tags.
          </p>
        </div>
      </div>
      <div>
        <div className="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="prose lg:prose-xl space-y-4">
            <p>
              With Atlus, simply input your raw address data, and let our
              advanced algorithms do the heavy lifting. Our intelligent parsing
              technology meticulously analyzes each address, extracting vital
              components such as street names, city names, postal codes, and
              more, all seamlessly compatible with OpenStreetMap standards.
            </p>
            <p>
              Say goodbye to tedious manual tagging and hello to streamlined
              efficiency. Whether you're managing large-scale mapping projects,
              optimizing logistics operations, or enhancing location-based
              services, Atlus empowers you to unlock the full potential of your
              address data with unparalleled accuracy and speed.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
