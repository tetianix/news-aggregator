#include <iostream>
#include <string>
#include <vector>

#include <httplib.h>
#include <nlohmann/json.hpp>

#include "keyword_rule.h"
#include "rule_engine.h"

using json = nlohmann::json;

int main(int argc, char* argv[]) {
    int port = argc > 1 ? std::stoi(argv[1]) : 8080;

    httplib::Server server;
    RuleEngine engine;

    server.Get("/health", [](const httplib::Request&, httplib::Response& res) {
        res.set_content(R"({"status":"ok"})", "application/json");
    });

    server.Post("/filter", [&engine](const httplib::Request& req, httplib::Response& res) {
        try {
            json body = json::parse(req.body);
            KeywordRule rule(body.at("keyword").get<std::string>());

            std::vector<ArticleText> articles;
            for (const auto& item : body.at("articles")) {
                articles.push_back({item.at("id").get<std::string>(), item.at("text").get<std::string>()});
            }

            json result;
            result["matched"] = engine.filter(articles, rule);
            res.set_content(result.dump(), "application/json");
        } catch (const std::exception& e) {
            res.status = 400;
            res.set_content(json{{"error", e.what()}}.dump(), "application/json");
        }
    });

    std::cout << "Rule server: http://127.0.0.1:" << port << std::endl;
    server.listen("127.0.0.1", port);
    return 0;
}
