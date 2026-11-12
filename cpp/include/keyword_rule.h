#pragma once

#include <string>

#include "rule.h"

class KeywordRule : public Rule {
public:
    explicit KeywordRule(std::string keyword);
    bool matches(const ArticleText& article) const override;

private:
    std::string keyword_;
};
