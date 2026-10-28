cask "copy-paste-manager" do
  version "2.0.5,3"
  sha256 "df154323cc96b45ee9f998abd36394f2c60d2fe03ea84080409fadfc36170ae5"

  url "https://github.com/pandailan/copy-paste-manager/releases/download/v#{version.csv.first}-#{version.csv.second}/Copy-Paste-Manager-#{version.csv.first}-#{version.csv.second}.zip"
  name "Copy Paste Manager"
  desc "Private clipboard history with search, collections, and paste workflows"
  homepage "https://copypastemanager.com/"

  livecheck do
    url :url
    regex(/^v?(\d+(?:\.\d+)+)-(\d+)$/i)
    strategy :github_releases do |json, regex|
      json.filter_map do |release|
        next if release["draft"]

        match = release["tag_name"]&.match(regex)
        "#{match[1]},#{match[2]}" if match
      end
    end
  end

  depends_on macos: :sonoma

  app "Copy Paste Manager.app"
end
