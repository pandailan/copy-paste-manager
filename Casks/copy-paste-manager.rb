cask "copy-paste-manager" do
  version "2.0.5,3"
  sha256 "df154323cc96b45ee9f998abd36394f2c60d2fe03ea84080409fadfc36170ae5"

  url "https://github.com/pandailan/copy-paste-manager/releases/download/v#{version.csv.first}-#{version.csv.second}/Copy-Paste-Manager-#{version.csv.first}-#{version.csv.second}.zip",
      verified: "github.com/pandailan/copy-paste-manager/"
  name "Copy Paste Manager"
  desc "Private clipboard history with search, collections, and paste workflows"
  homepage "https://copypastemanager.com/"

  depends_on macos: :sonoma

  app "Copy Paste Manager.app"
end
